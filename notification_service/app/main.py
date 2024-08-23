from fastapi import FastAPI
from app.kafka.consumers.order_consumer import consume_order_messages
import asyncio

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(consume_order_messages())

@app.get("/")
def root():
    return {"message": "Email Service is running!"}
