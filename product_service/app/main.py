from fastapi import FastAPI, Depends, HTTPException
from aiokafka import AIOKafkaProducer
from sqlmodel import Session
from .database import get_session, init_db
from .crud.product import create_product, get_product, update_product, delete_product
from .kafka.producers.product_producer import publish_message
from .kafka.consumers.product_consumer import consume_messages
from .models import ProductCreate, ProductRead
import asyncio

app = FastAPI(title="Product Service", version="0.0.1")

@app.on_event("startup")
async def on_startup():
    init_db()
    asyncio.create_task(consume_messages())

async def get_kafka_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/products/", response_model=ProductRead)
async def create_product_view(product: ProductCreate, session: Session = Depends(get_session), producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    db_product = create_product(session, product)
    await publish_message(producer, "create", db_product, product.quantity)
    return ProductRead.from_orm(db_product)

@app.put("/products/{product_id}", response_model=ProductRead)
async def update_product_view(product_id: int, product: ProductCreate, session: Session = Depends(get_session), producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    db_product = update_product(session, product_id, product)
    await publish_message(producer, "update", db_product, product.quantity)
    return db_product

@app.delete("/products/{product_id}", status_code=204)
async def delete_product_view(product_id: int, session: Session = Depends(get_session), producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    delete_product(session, product_id)
    message = {
        "action": "delete",
        "id": product_id
    }
    try:
        await producer.send_and_wait(KAFKA_PRODUCT_TOPIC, json.dumps(message).encode("utf-8"))
        print(f"Message sent to Kafka: {message}")
    except Exception as e:
        print(f"Failed to send message to Kafka: {str(e)}")
    return None