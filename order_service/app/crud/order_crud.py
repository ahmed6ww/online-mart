from typing import List, Optional
from sqlmodel import Session, select
from app.models import User, UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.exec(select(User).where(User.id == user_id)).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.exec(select(User).offset(skip).limit(limit)).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.exec(select(User).where(User.id == user_id)).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = db.exec(select(User).where(User.id == user_id)).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
