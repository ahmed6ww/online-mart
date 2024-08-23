import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from sqlmodel import Session
from app import settings
from app.database import engine
from app.models import Payment, Order

async def consume_order_messages():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_ORDER_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT,
        auto_offset_reset='latest'
    )
    
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL
    )
    
    await consumer.start()
    await producer.start()
    try:
        async for message in consumer:
            try:
                order_data = json.loads(message.value.decode())
                print("Received order message:", order_data)
                
                # Extract details from the message
                order_id = order_data.get('id')
                product_id = order_data.get('product_id')
                quantity = order_data.get('quantity')
                total_amount = order_data.get('total_amount')
                
                if not order_id or not product_id or not quantity:
                    print("Missing required fields in order message:", order_data)
                    continue
                
                # Simulate payment processing
                payment_successful = process_payment(order_id, total_amount)
                
                # Insert payment record into the payment database
                with Session(engine) as session:
                    payment_record = Payment(
                        order_id=order_id,
                        product_id=product_id,
                        name=order_data.get('user_full_name'),
                        status="Paid" if payment_successful else "Failed",
                        amount=total_amount
                    )
                    session.add(payment_record)
                    session.commit()
                    print(f"Payment record created for order_id: {order_id}")

                if payment_successful:
                    # Produce a message to update the order status
                    payment_message = {
                        'id': order_id,
                        'status': 'Paid'
                    }
                    # await producer.send_and_wait(settings.KAFKA_PAYMENT_TOPIC, value=json.dumps(payment_message).encode())
                    # print(f"Payment processed and status updated for order_id: {order_id}")
                else:
                    print(f"Payment failed for order_id: {order_id}")
            
            except json.JSONDecodeError:
                print("Failed to decode JSON from message:", message.value.decode())
            except KeyError as e:
                print(f"KeyError: Missing key {e} in message:", message.value.decode())
            except Exception as e:
                print(f"Unexpected error: {e}")

    finally:
        await producer.stop()
        await consumer.stop()

def process_payment(order_id: int, total_amount: float) -> bool:
    # Simulate a payment processing logic
    # This could be an API call to a payment gateway
    print(f"Processing payment for order_id: {order_id} with amount: {total_amount}")
    return True  # Simulating success; replace with actual payment logic
