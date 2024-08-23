from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    email: str = Field(sa_column_kwargs={"unique": True})
    password: str
    full_name: str
    address: str  # Fixed typo from "adress" to "address"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    address: str

class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    address: str
