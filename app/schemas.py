from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# City schemas
class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    additional_info: Optional[str] = None


class City(CityBase):
    id: int
    temperatures_count: Optional[int] = 0

    class Config:
        from_attributes = True


# Temperature schemas
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        from_attributes = True


# Response schemas
class TemperatureWithCity(Temperature):
    city_name: str

    class Config:
        from_attributes = True
