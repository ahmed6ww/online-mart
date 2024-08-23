import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session, init_db
from app.models import OrderModel, OrderUpdate
from app.kafka.producers.order_producer import publish_order_message
from app.kafka.consumers.order_consumer import consume_order_messages
from aiokafka import AIOKafkaProducer
from app import settings

app = FastAPI(title="Order Service", version="0.0.1")

# Initialize the database
init_db()

@app.post("/orders/", response_model=OrderModel)
async def create_order(order: OrderModel):
    # Create an instance of AIOKafkaProducer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL
    )
    
    # Start the producer
    await producer.start()

    try:
        # Prepare the order data dictionary
        order_data = {
            
            "user_id": order.user_id,
            "user_email": order.user_email,
            "user_full_name": order.user_full_name,
            "user_address": order.user_address,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_amount": order.total_amount,
            "product_title": order.product_title,
            "product_description": order.product_description,
            "product_category": order.product_category,
            "product_brand": order.product_brand,
            "status": order.status,
        }

        # Publish the order message
        await publish_order_message(producer, order_data)
        

    finally:
        # Stop the producer
        await producer.stop()

    return {"message": "Order created and message published successfully"}

@app.put("/orders/{order_id}", response_model=OrderModel)
async def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_session)):
    order = db.get(OrderModel, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

# Consumer to run as a background task
@app.on_event("startup")
async def start_kafka_consumer():
    asyncio.create_task(consume_order_messages())
