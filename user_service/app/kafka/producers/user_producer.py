import json
from aiokafka import AIOKafkaProducer
from app import settings
from app.models import UserCreate

async def publish_user_message(producer: AIOKafkaProducer, action: str, user: UserCreate):
    message = {
        "action": action,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "full_name": user.full_name,
        "address": user.address
    }
    try:
        await producer.send_and_wait(settings.KAFKA_USER_TOPIC, json.dumps(message).encode("utf-8"))
        print(f"Message sent to Kafka: {message}")
    except Exception as e:
        print(f"Failed to send message to Kafka: {str(e)}")
