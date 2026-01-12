from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    """Create a new city"""
    # Check if city already exists
    existing_city = db.query(crud.models.City).filter(
        crud.models.City.name == city.name
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.City])
def read_cities(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get all cities"""
    cities = crud.get_cities(db, skip=skip, limit=limit)

    # Add temperatures count to each city
    for city in cities:
        city.temperatures_count = crud.get_temperature_count_by_city(db, city.id)

    return cities


@router.get("/", response_model=List[schemas.CityWithCount])
def read_cities(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get all cities with temperature counts in a single query"""
    # Single optimized query using LEFT JOIN and GROUP BY
    cities_with_counts = db.query(
        models.City,
        func.count(models.Temperature.id).label('temperatures_count')
    ).outerjoin(
        models.Temperature,
        models.City.id == models.Temperature.city_id
    ).group_by(
        models.City.id
    ).order_by(
        models.City.id
    ).offset(skip).limit(limit).all()

    # Convert to response models
    result = []
    for city, count in cities_with_counts:
        city_data = schemas.CityWithCount.model_validate(city)
        city_data.temperatures_count = count
        result.append(city_data)

    return result


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    """Update a city"""
    db_city = crud.update_city(db, city_id, city_update)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    db_city.temperatures_count = crud.get_temperature_count_by_city(db, city_id)
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    """Delete a city"""
    if not crud.delete_city(db, city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return None
