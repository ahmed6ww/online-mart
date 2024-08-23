import json
from aiokafka import AIOKafkaProducer
from app import settings
from app.models import ProductRead

async def publish_message(producer: AIOKafkaProducer, action: str, product: ProductRead, quantity: int):
    message = {
        "action": action,
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "quantity": quantity
    }
    try:
        await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, json.dumps(message).encode("utf-8"))
        print(f"Message sent to Kafka: {message}")
    except Exception as e:
        print(f"Failed to send message to Kafka: {str(e)}")
