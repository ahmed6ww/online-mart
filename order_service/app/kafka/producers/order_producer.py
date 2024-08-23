import json
from aiokafka import AIOKafkaProducer
from app import settings

async def publish_order_message(producer: AIOKafkaProducer, order_data: dict):
    try:
        await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, json.dumps(order_data).encode("utf-8"))
        print(f"Order message sent to Kafka: {order_data}")
    except Exception as e:
        print(f"Failed to send order message to Kafka: {str(e)}")
