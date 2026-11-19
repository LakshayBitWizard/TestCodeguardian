# HealthSync — Patient Record Management API

A FastAPI-based backend for managing patient records, appointments,
prescriptions, and billing in a multi-clinic healthcare network.

## Tech Stack
- **Backend**: Python 3.11 / FastAPI
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Auth**: JWT token-based authentication

## Quick Start
```bash
pip install -r requirements.txt
uvicorn api.patient_routes:app --reload --port 8080
```

## Project Structure
```
config/          → Application settings and secrets
models/          → Data models and ORM definitions
services/        → Core business logic layer
api/             → REST API route handlers
utils/           → Reporting and migration utilities
tests/           → Unit and integration tests
```
