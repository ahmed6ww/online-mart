import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
from app.database import Session, engine
from app.models import InventoryMessage
from app.settings import KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY, KAFKA_BROKER_URL, KAFKA_BROKER_URL, KAFKA_INVENTORY_TOPIC
from app.crud.inventory_crud import create_or_update_inventory, delete_inventory
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def process_message(message_value: str, session: Session):
    try:
        message_data = json.loads(message_value)
        logger.info(f"Processing message: {message_data}")
        action = message_data.get("action")
        product_id = message_data.get("id")
        product_name = message_data.get("name")
        quantity = message_data.get("quantity", 0)  # Default to 0 if not provided

        if action == "create" or action == "update":
            create_or_update_inventory(session, product_id, product_name, quantity)
        elif action == "delete":
            delete_inventory(session, product_id)
        else:
            logger.warning(f"Unknown action: {action}")
        
        # Store message in the database for tracking
        new_message = InventoryMessage(message=message_value, topic="inventory")
        session.add(new_message)
        session.commit()
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        KAFKA_INVENTORY_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        async for message in consumer:
            logger.info(f"Received message: {message.value.decode()} on topic {message.topic}")
            with Session(engine) as session:
                await process_message(message.value.decode(), session)
    finally:
        await consumer.stop()