from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from datetime import datetime


# City CRUD operations
def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city_by_id(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate) -> Optional[models.City]:
    db_city = get_city_by_id(db, city_id)
    if not db_city:
        return None

    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city_by_id(db, city_id)
    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True


# Temperature CRUD operations
def create_temperature(db: Session, temperature: schemas.TemperatureCreate) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[
    models.Temperature]:
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit).all()


def get_temperature_count_by_city(db: Session, city_id: int) -> int:
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).count()
