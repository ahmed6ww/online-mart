import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlmodel import Session
from app.database import engine
from app.models import OrderModel
from app import settings
from app.kafka.producers.payment_producer import publish_payment_message

async def consume_order_messages():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_ORDER_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset='latest'
    )
    
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URL)
    await consumer.start()
    await producer.start()
    
    try:
        async for message in consumer:
            print(f"Received order message: {message.value.decode()} on topic {message.topic}")
            with Session(engine) as session:
                await store_order(session, message, producer)
    finally:
        await consumer.stop()
        await producer.stop()

async def store_order(session: Session, message, producer: AIOKafkaProducer):
    try:
        # Decode and validate the message
        order_data = json.loads(message.value.decode())
        
        # Validate required fields before proceeding
        if not all(key in order_data for key in ['id', 'product_id', 'total_amount', 'user_full_name']):
            raise ValueError("Missing required fields in order message.")
        
        # Initialize OrderModel object
        new_order = OrderModel(**order_data)
        
        # Handle the case where id might be 0 (optional, depending on your database setup)
 
        # Add the new order to the session and commit it
        session.add(new_order)
        session.commit()
        print(f"Order stored in the database: {new_order}")
        
        # Prepare payment data for publishing
        payment_data = {
            "order_id": new_order.id,
            "status": "paid",
            "amount": new_order.total_amount,
            "product_id": new_order.product_id,
            "name": new_order.user_full_name,
        }
        
        # Publish payment message to Kafka
        await publish_payment_message(producer, payment_data)
        
    except json.JSONDecodeError:
        print("Failed to decode JSON from message.")
    except ValueError as e:
        print(f"Validation error: {str(e)}")
    except Exception as e:
        session.rollback()
        print(f"Failed to store order: {str(e)}")
