from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import time

from app.crud.restaurant import (
    get_restaurants,
    get_restaurant,
    create_restaurant,
    update_restaurant,
    delete_restaurant,
    get_restaurants_by_owner
)
from app.schemas.restaurant import (
    Restaurant,
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantSearchResults,
    CuisineType,
    PriceRange
)
from app.database import get_db
from app.core.security import get_current_active_user, has_role
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=RestaurantSearchResults)
def read_restaurants(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    cuisine_types: Optional[List[CuisineType]] = Query(None),
    price_ranges: Optional[List[PriceRange]] = Query(None),
    is_open_now: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve restaurants with optional filters.
    """
    restaurants = get_restaurants(
        db,
        skip=skip,
        limit=limit,
        search=search,
        cuisine_types=cuisine_types,
        price_ranges=price_ranges,
        is_open_now=is_open_now
    )
    total = len(restaurants)  # En producción usarías count con los mismos filtros
    return {"results": restaurants, "total": total}

@router.post("/", response_model=Restaurant, status_code=status.HTTP_201_CREATED)
def create_new_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role(UserRole.RESTAURANT_OWNER))
):
    """
    Create a new restaurant (only for restaurant owners).
    """
    return create_restaurant(db=db, restaurant=restaurant, owner_id=current_user.id)

@router.get("/my-restaurants", response_model=List[Restaurant])
def get_my_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(has_role(UserRole.RESTAURANT_OWNER))
):
    """
    Get restaurants owned by the current user.
    """
    return get_restaurants_by_owner(db, owner_id=current_user.id)

@router.get("/{restaurant_id}", response_model=Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Get a specific restaurant by ID.
    """
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@router.put("/{restaurant_id}", response_model=Restaurant)
def update_existing_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a restaurant (only for owner or admin).
    """
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Verificar si el usuario es el dueño o un admin
    if db_restaurant.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)

@router.delete("/{restaurant_id}")
def delete_existing_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a restaurant (only for owner or admin).
    """
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Verificar si el usuario es el dueño o un admin
    if db_restaurant.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    delete_restaurant(db=db, restaurant_id=restaurant_id)
    return {"message": "Restaurant deleted successfully"}