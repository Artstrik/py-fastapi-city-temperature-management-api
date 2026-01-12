from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import asyncio
from .. import schemas, crud, dependencies
from ..database import get_db
from ..services.weather_service import weather_service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", status_code=status.HTTP_202_ACCEPTED)
async def update_temperatures(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """Fetch and store current temperatures for all cities"""
    cities = crud.get_cities(db)

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in database"
        )

    # Prepare city data for API calls
    city_data = [{"id": city.id, "name": city.name} for city in cities]

    # Fetch temperatures asynchronously
    temperature_data = await weather_service.fetch_temperatures_for_cities(city_data)

    # Store temperatures in database
    for temp_data in temperature_data:
        temperature_create = schemas.TemperatureCreate(**temp_data)
        crud.create_temperature(db, temperature_create)

    return {
        "message": f"Successfully updated temperatures for {len(temperature_data)} cities",
        "updated_count": len(temperature_data)
    }


@router.get("/", response_model=List[schemas.TemperatureWithCity])
def read_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city ID"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get temperature records, optionally filtered by city"""
    temperatures = crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)

    # Enrich with city name
    result = []
    for temp in temperatures:
        temp_dict = schemas.Temperature.from_orm(temp).model_dump()
        temp_dict["city_name"] = temp.city.name
        result.append(temp_dict)

    return result
