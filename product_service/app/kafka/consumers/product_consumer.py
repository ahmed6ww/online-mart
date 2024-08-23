import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from app.models import ProductMessage
from app.database import engine
from app.settings import KAFKA_BROKER_URL, KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT, KAFKA_INVENTORY_TOPIC

async def consume_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_INVENTORY_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT,
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
