
from sqlmodel import SQLModel, Field

class OrderModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    user_email: str | None
    user_full_name: str | None
    user_address: str | None
    product_id: int
    quantity: int
    total_amount: float | None
    product_title: str | None
    product_description: str | None
    product_category: str | None
    product_brand: str | None
    status : str = Field(default="Unpaid")

class OrderUpdate(SQLModel):
    # user_id: int | None = None
    quantity: int | None = None
    total_amount: float | None = None
    status : str | None = Field(default="Unpaid")
    # status: OrderStatus | None = None