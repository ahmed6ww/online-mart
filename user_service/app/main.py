from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session
from app.models import UserCreate, User
from app.kafka.producers.user_producer import publish_user_message
from app.kafka.consumers.user_consumer import consume_user_messages
from app import settings
from app.database import engine, init_db
from aiokafka import AIOKafkaProducer

app = FastAPI()

# Initialize the database


@app.post("/register/")
async def register_user(user: UserCreate):
    # Create a Kafka producer instance
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL,
    )
    
    await producer.start()
    try:
        # Define the action for the Kafka message
        action = "register"
        
        # Publish user registration message to Kafka
        await publish_user_message(producer, action, user)
    finally:
        await producer.stop()
    
    return {"status": "User registration message sent"}
@app.on_event("startup")
async def on_startup():
    # Start Kafka consumer
    init_db()
    import asyncio
    asyncio.create_task(consume_user_messages())

@app.on_event("shutdown")
def on_shutdown():
    # Cleanup code if needed
    pass
