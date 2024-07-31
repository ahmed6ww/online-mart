from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float

class ProductMessage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    message: str
    topic: str