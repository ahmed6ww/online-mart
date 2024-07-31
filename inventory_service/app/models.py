from sqlmodel import SQLModel, Field

class InventoryMessage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    message: str
    topic: str
