from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from sqlmodel import SQLModel, Field, Session
from .database import get_session, init_db, engine
from .models import ProductMessage
app = FastAPI(
    title="Kafka Template",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000",
            "description": "Development Server"
        }
    ]
)

KAFKA_BROKER_URL = "broker:19092"
TOPIC_NAME = "Products"


async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="products-group",
        auto_offset_reset='latest'
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            with Session(engine) as session:
                store_message(session, message)
    finally:
        await consumer.stop()

def store_message(session: Session, message):
    new_message = ProductMessage(
        message=message.value.decode(),
        topic=message.topic
    )
    session.add(new_message)
    session.commit()

@app.on_event("startup")
async def start_consumer():
    init_db()
    asyncio.create_task(consume_messages(TOPIC_NAME, KAFKA_BROKER_URL))

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield

@app.get("/")
def read_root():
    return {"Name": "Product Service", "Message": "Use this service for product management"}

async def get_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/produce/")
async def produce_message(message: str, producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    try:
        await producer.send_and_wait(TOPIC_NAME, message.encode("utf-8"))
        return {"status": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
