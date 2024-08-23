from sqlmodel import Session, select
from app.models import Order

def get_latest_order_by_product_and_name(session: Session, product_id: int, name: str) -> Order:
    statement = select(Order).where(Order.product_id == product_id, Order.name == name).order_by(Order.id.desc())
    return session.exec(statement).first()
