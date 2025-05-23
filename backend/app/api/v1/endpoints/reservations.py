from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.crud.reservation import (
    create_reservation,
    get_reservation,
    get_reservations_by_user,
    get_reservations_by_restaurant,
    update_reservation,
    delete_reservation
)
from app.schemas.reservation import (
    Reservation,
    ReservationCreate,
    ReservationUpdate,
    ReservationStatus
)
from app.database import get_db
from app.core.security import get_current_active_user, has_role
from app.models.user import UserRole

router = APIRouter()

@router.post("/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation_endpoint(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return create_reservation(db=db, reservation=reservation, user_id=current_user.id)

@router.get("/user", response_model=List[Reservation])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return get_reservations_by_user(db, user_id=current_user.id)

@router.get("/restaurant/{restaurant_id}", response_model=List[Reservation])
def get_restaurant_reservations(
    restaurant_id: int,
    date: datetime = None,
    db: Session = Depends(get_db),
    current_user = Depends(has_role(UserRole.RESTAURANT_OWNER))
):
    return get_reservations_by_restaurant(db, restaurant_id=restaurant_id, date=date)

@router.put("/{reservation_id}", response_model=Reservation)
def update_reservation_endpoint(
    reservation_id: int,
    reservation: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_reservation = get_reservation(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Solo el dueño o el administrador puede actualizar
    if db_reservation.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return update_reservation(db=db, reservation_id=reservation_id, reservation=reservation)

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_reservation = get_reservation(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if db_reservation.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    delete_reservation(db=db, reservation_id=reservation_id)
    return None