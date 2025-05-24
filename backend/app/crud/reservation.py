from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from typing import List, Optional

def get_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
    """Obtiene una reserva por ID"""
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    restaurant_id: Optional[int] = None,
    user_id: Optional[int] = None,
    date: Optional[date] = None,
    status: Optional[str] = None
) -> list[Reservation]:
    """Lista reservas con filtros"""
    query = db.query(Reservation)
    
    if restaurant_id:
        query = query.filter(Reservation.restaurant_id == restaurant_id)
    
    if user_id:
        query = query.filter(Reservation.user_id == user_id)
    
    if date:
        query = query.filter(
            and_(
                Reservation.date_time >= datetime.combine(date, datetime.min.time()),
                Reservation.date_time < datetime.combine(date, datetime.max.time())
            )
        )
    
    if status:
        query = query.filter(Reservation.status == status)
    
    return query.offset(skip).limit(limit).all()

def create_reservation(
    db: Session, 
    reservation: ReservationCreate, 
    user_id: int
) -> Reservation:
    """Crea una nueva reserva"""
    db_reservation = Reservation(**reservation.dict(), user_id=user_id)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_reservation(
    db: Session, 
    reservation_id: int, 
    reservation: ReservationUpdate
) -> Optional[Reservation]:
    """Actualiza una reserva existente"""
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        update_data = reservation.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: int) -> bool:
    """Elimina una reserva"""
    db_reservation = get_reservation(db, reservation_id)
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
        return True
    return False

def get_reservations_by_user(
    db: Session, 
    user_id: int
) -> list[Reservation]:
    """Obtiene todas las reservas de un usuario"""
    return get_reservations(db, user_id=user_id)

def get_reservations_by_restaurant(
    db: Session, 
    restaurant_id: int,
    date: Optional[date] = None
) -> list[Reservation]:
    """Obtiene todas las reservas de un restaurante"""
    return get_reservations(db, restaurant_id=restaurant_id, date=date)