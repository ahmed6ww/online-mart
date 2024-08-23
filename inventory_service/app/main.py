from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from typing import List
from aiokafka import AIOKafkaConsumer
from .models import Inventory, InventoryMessage
from .database import get_session, init_db, engine
from .settings import KAFKA_BROKER_URL, KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY
from app.kafka.consumers.inventory_consumer import consume_messages
import asyncio
import json
import logging

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





@app.on_event("startup")
async def on_startup():
    init_db()
    asyncio.create_task(consume_messages("Products", KAFKA_BROKER_URL))
    asyncio.create_task(consume_messages("Orders", KAFKA_BROKER_URL))

@app.get("/")
def read_root():
    return {"Name": "Inventory Service", "Message": "Use this service for inventory management"}