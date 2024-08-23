from sqlmodel import SQLModel, Field

class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"  # Ensure the table name is explicitly defined
    __table_args__ = {"extend_existing": True}  # This allows redefining the table

    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(index=True)
    product_name: str = Field(index=True, nullable=False)  # Ensure `nullable=False` is set
    quantity: int

class InventoryMessage(SQLModel, table=True):
    __tablename__ = "inventory_message"  # Ensure the table name is explicitly defined
    __table_args__ = {"extend_existing": True}  # This allows redefining the table

    id: int = Field(default=None, primary_key=True)
    message: str
    topic: str
