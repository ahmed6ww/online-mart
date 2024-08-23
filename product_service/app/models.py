from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Product(SQLModel, table=True):
    __tablename__ = "product"
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int

class ProductRead(SQLModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int  # Add quantity if it's part of the creation process

class ProductMessage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    message: str
    topic: str