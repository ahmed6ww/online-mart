from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from .settings import DATABASE_URL

# Create the database engine using the configuration from settings.py
engine = create_engine(str(DATABASE_URL), echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Function to initialize the database
def init_db():
    SQLModel.metadata.create_all(engine)
