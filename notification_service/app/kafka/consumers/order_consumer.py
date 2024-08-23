# app/kafka/consumers/order_consumer.py
import asyncio
from aiokafka import AIOKafkaConsumer
import json
from app.email.email_sender import send_order_confirmation_email
from app.settings import KAFKA_BROKER_URL, KAFKA_ORDER_TOPIC, KAFKA_CONSUMER_GROUP_ID_FOR_ORDER

async def consume_order_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_ORDER_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            order = json.loads(message.value.decode())
            print(f"Order details: {order}")
            
            product_id = order['product_id']
            quantity = order['quantity']
            
            # Email details
            to_email = "ahmed369ww@gmail.com"  # For testing, hard-coded email
            subject = "Order Confirmation"
            body = f"Your order for product ID {product_id} with quantity {quantity} has been placed successfully."
            
            # Send email
            send_order_confirmation_email(to_email, subject, body)
    finally:
        await consumer.stop()

