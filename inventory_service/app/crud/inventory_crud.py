import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
from app.database import Session, engine
from app.models import InventoryMessage, Inventory
from app.settings import KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY, KAFKA_BROKER_URL, KAFKA_INVENTORY_TOPIC
from sqlmodel import select
import logging






# CRUD Operations
def create_or_update_inventory(session: Session, product_id: int, product_name: str, quantity: int) -> Inventory:
    inventory = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()

    if inventory:
        # Update existing inventory
        logger.info(f"Updating inventory: {inventory}")
        inventory.quantity += quantity
        inventory.product_name = product_name
    else:
        # Create new inventory record
        inventory = Inventory(product_id=product_id, product_name=product_name, quantity=quantity)

    try:
        session.add(inventory)
        session.commit()
        session.refresh(inventory)
        logger.info(f"Inventory updated successfully: {inventory}")
        return inventory
    except Exception as e:
        logger.error(f"Error updating inventory: {e}")
        raise HTTPException(status_code=500, detail="Error updating inventory")

def delete_inventory(session: Session, product_id: int) -> None:
    inventory = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if inventory:
        try:
            session.delete(inventory)
            session.commit()
            logger.info(f"Inventory deleted successfully: {inventory}")
        except Exception as e:
            logger.error(f"Error deleting inventory: {e}")
            raise HTTPException(status_zzzzzcode=500, detail="Error deleting inventory")
    else:
        raise HTTPException(status_code=404, detail="Inventory not found")