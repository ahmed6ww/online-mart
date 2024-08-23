from sqlmodel import SQLModel, Field
from datetime import datetime

class Payment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int
    product_id: int
    name: str
    status: str
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int
    name: str
    quantity: int
    status: str
