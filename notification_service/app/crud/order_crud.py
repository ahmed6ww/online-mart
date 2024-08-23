from sqlmodel import Session
from app.models import Order

async def save_order(session: Session, product_id: int, quantity: int):
    order = Order(product_id=product_id, quantity=quantity, status="created")
    session.add(order)
    session.commit()
