from pydantic import BaseModel, Field, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

# Temperature schemas
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)

# Response schemas
class CityWithCount(City):
    """City schema with temperature count included"""
    temperatures_count: int = 0

class TemperatureWithCity(Temperature):
    """Temperature schema with city name included"""
    city_name: str
    model_config = ConfigDict(from_attributes=True)
