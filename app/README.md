# City Temperature Management System

A FastAPI application for managing cities and their temperature data with real-time weather updates.

## Features

- **City Management**: Full CRUD operations for cities
- **Temperature Tracking**: Record and retrieve temperature data
- **Real-time Weather Updates**: Fetch current temperatures from OpenWeatherMap API
- **Database Migrations**: Using Alembic for schema management
- **Async Operations**: Non-blocking API calls for weather data

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd city-temperature-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key (optional)
alembic init migrations
# Copy the provided alembic.ini and migrations/env.py files
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
