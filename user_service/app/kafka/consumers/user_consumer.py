import json
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session, SQLModel
from app.models import User, UserCreate
from app.settings import KAFKA_BROKER_URL, KAFKA_CONSUMER_GROUP_ID_FOR_USER, KAFKA_USER_TOPIC
from app.database import engine

async def consume_user_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_USER_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_USER,
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            with Session(engine) as session:
                store_user(session, message)
    finally:
        await consumer.stop()

def store_user(session: Session, message):
    try:
        message_data = json.loads(message.value.decode())
        
        # Log the incoming data
        print(f"Processing message data: {message_data}")
        
        user_data = UserCreate(**message_data)
        
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            address=user_data.address
        )
        
        session.add(new_user)
        session.commit()
        print(f"User stored in the database: {new_user}")
    except Exception as e:
        # Log the error in detail
        print(f"Failed to store user: {str(e)}")
        session.rollback()
        print("Transaction has been rolled back.")
    finally:
        session
