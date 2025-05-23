from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime, time
from ..models.restaurant import Restaurant
from ..schemas.restaurant import RestaurantCreate, RestaurantUpdate
from typing import List, Optional

def get_restaurants(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[List] = None,
    search: Optional[str] = None,
    cuisine_types: Optional[List[str]] = None,
    price_ranges: Optional[List[int]] = None,
    is_open_now: Optional[bool] = None
):
    query = db.query(Restaurant)
    
    # Aplicar filtros básicos
    if filters:
        for filter in filters:
            query = query.filter(filter)
    
    # Búsqueda por nombre o dirección
    if search:
        query = query.filter(
            or_(
                Restaurant.name.ilike(f"%{search}%"),
                Restaurant.address.ilike(f"%{search}%"),
                Restaurant.description.ilike(f"%{search}%")
            )
        )
    
    # Filtro por tipo de cocina
    if cuisine_types:
        query = query.filter(Restaurant.cuisine_type.in_(cuisine_types))
    
    # Filtro por rango de precios
    if price_ranges:
        query = query.filter(Restaurant.price_range.in_(price_ranges))
    
    # Filtro por restaurantes abiertos ahora
    if is_open_now:
        now = datetime.now().time()
        query = query.filter(
            and_(
                Restaurant.opening_time <= now,
                Restaurant.closing_time >= now
            )
        )
    
    return query.offset(skip).limit(limit).all()

def get_restaurant(db: Session, restaurant_id: int):
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

def create_restaurant(db: Session, restaurant: RestaurantCreate, owner_id: int):
    db_restaurant = Restaurant(**restaurant.dict(), owner_id=owner_id)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant(db: Session, restaurant_id: int, restaurant: RestaurantUpdate):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        update_data = restaurant.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_restaurant, key, value)
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant

def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        db.delete(db_restaurant)
        db.commit()
        return True
    return False

def get_restaurants_by_owner(db: Session, owner_id: int):
    return db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()