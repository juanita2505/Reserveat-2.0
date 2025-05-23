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
def search_restaurants(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    cuisine_types: Optional[List[CuisineType]] = Query(None),
    price_ranges: Optional[List[PriceRange]] = Query(None),
    is_open_now: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Search restaurants with filters
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
    return {"results": restaurants, "total": len(restaurants)}

@router.post("/", response_model=Restaurant, status_code=status.HTTP_201_CREATED)
def create_restaurant_endpoint(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user = Depends(has_role(UserRole.RESTAURANT_OWNER))
):
    return create_restaurant(db=db, restaurant=restaurant, owner_id=current_user.id)

@router.get("/my-restaurants", response_model=List[Restaurant])
def get_my_restaurants(
    db: Session = Depends(get_db),
    current_user = Depends(has_role(UserRole.RESTAURANT_OWNER))
):
    return get_restaurants_by_owner(db, owner_id=current_user.id)

@router.get("/{restaurant_id}", response_model=Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@router.put("/{restaurant_id}", response_model=Restaurant)
def update_restaurant_endpoint(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)

@router.delete("/{restaurant_id}")
def delete_restaurant_endpoint(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_restaurant = get_restaurant(db, restaurant_id=restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    delete_restaurant(db=db, restaurant_id=restaurant_id)
    return {"message": "Restaurant deleted successfully"}