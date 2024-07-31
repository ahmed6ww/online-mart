from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer
import asyncio
from .database import get_session, init_db, engine
from .models import InventoryMessage
app = FastAPI(
    title="Inventory Service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8002",
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
        group_id="inventory-group",
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
    new_message = InventoryMessage(
        message=message.value.decode(),
        topic=message.topic
    )
    session.add(new_message)
    session.commit()

@app.on_event("startup")
async def start_consumer():
    init_db()
    asyncio.create_task(consume_messages(TOPIC_NAME, KAFKA_BROKER_URL))

@app.get("/")
def read_root():
    return {"Name": "Inventory Service", "Message": "Use this service for inventory management"}
