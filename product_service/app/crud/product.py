from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List, Optional
from ..models import Product, ProductCreate

def create_product(session: Session, product: ProductCreate) -> Product:
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def get_product(session: Session, product_id: int) -> Optional[Product]:
    return session.exec(select(Product).where(Product.id == product_id)).first()

def get_products(session: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    return session.exec(select(Product).offset(skip).limit(limit)).all()

def update_product(session: Session, product_id: int, product: ProductCreate) -> Product:
    db_product = get_product(session, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        if hasattr(db_product, key):
            setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def delete_product(session: Session, product_id: int) -> None:
    db_product = get_product(session, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(db_product)
    session.commit()
