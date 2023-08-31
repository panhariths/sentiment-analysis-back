#!/bin/bash

# Run Alembic migration
alembic upgrade head

# Start FastAPI using Uvicorn
uvicorn main:main --reload --host 0.0.0.0 --port 8000
