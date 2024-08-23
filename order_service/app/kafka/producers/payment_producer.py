import json
from aiokafka import AIOKafkaProducer
from app import settings

async def publish_payment_message(producer: AIOKafkaProducer, payment_data: dict):
    print(f"Publishing payment message to Kafka: {payment_data}")
    try:
        # Publish the payment message to the Kafka payment topic
        await producer.send_and_wait(settings.KAFKA_PAYMENT_TOPIC, json.dumps(payment_data).encode("utf-8"))
        print(f"Payment message sent to Kafka: {payment_data}")
    except Exception as e:
        print(f"Failed to send payment message to Kafka: {str(e)}")
