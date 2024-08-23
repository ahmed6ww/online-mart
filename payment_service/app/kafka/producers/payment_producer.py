import asyncio
from aiokafka import AIOKafkaProducer
import json
from app.settings import KAFKA_BROKER_URL, KAFKA_PAYMENT_TOPIC

async def produce_payment_message(order_id: int, product_name: str, status: str):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL
    )
    await producer.start()
    try:
        payment_message = {
            "order_id": order_id,
            "product_name": product_name,
            "status": status
        }
        await producer.send_and_wait(KAFKA_PAYMENT_TOPIC, json.dumps(payment_message).encode('utf-8'))
    finally:
        await producer.stop()
