FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc

# Copy the application code to the container
RUN mkdir -p /usr/src/fastapi-app
COPY . /usr/src/fastapi-app

# Set the working directory in the container
WORKDIR /usr/src/fastapi-app

# Install dependencies using poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
# RUN pip install alembic uvicorn

RUN chmod +x /usr/src/fastapi-app/startup.sh
# ENTRYPOINT /fastapi-app/docker/api/startup.sh
