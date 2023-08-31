# fastapi-boilerplate

Boilerplate template for FastAPI repositories

## Table of Contents

- [Pre-requisites](#pre-requisites)
  - [Poetry](#poetry)
  - [Enabling pre-commit hooks](#enabling-pre-commit-hooks)
- [Connecting with database](#Connecting with database)
  - [Creating migrations](#creating-migrations)
- [Docker Setup](#Docker Setup)
  - [Dockerfile](#Dockerfile)
  - [Docker-compose](#Docker-compose)

## Pre-requisites

### Poetry

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Create a virtual environment: `poetry install` this will create .venv in the root directory of your project. VScode will automatically detect this virtual environment and use it during dev.
**Note**: Use below command to add new dependencies to the project
`poetry add <package-name>=v1.2.3`, this will add the package to pyproject.toml and poetry.lock files.

### Enabling pre-commit hooks

Pre-commit hooks can help in improving the quality of your commits. It is a great way to ensure that the code that goes
to your VCS is clean and properly formatted. This boilerplate has a pre-commit-config file that defines some pre-commit
hooks which can be enabled by running the following command:

```
pip install pre-commit
pre-commit install
```

Thereafter, every time you commit, the pre-commit hooks will be executed and the commit will be aborted if any of the
formatter fails.

You can also run the pre-commit hooks manually by running the following command:

```
pre-commit run --all-files
```

## Connecting with database
This boilerplate uses Postgres database and SQLAlchemy as the ORM.
Create your database then create a user and grant all privileges to the user on that database.

Add database configurations (i-e; database name, user, pass) in the environment variables (refer to config.py file presented in config package for variable names)


### Creating migrations
This boilerplate uses Alembic for migrations.
To install alembic, run the following command:
```
 pip install alembic
```
To create a migration of your new model, follow the following steps:
1. Create new model(s) in your required package under models package.
2. Import new model(s) in env.py file placed in alembic package.
3. Run the following command to create a new migration:
```
 alembic revision --autogenerate -m "<migration file name>"
```
This will autogenerate a migration file in alembic/versions package.

### Running migrations
Run the following command to apply the migrations:
```
 alembic upgrade head
```

## Docker Setup
### Dockerfile
The boilerplate contains a Dockerfile which copies the source code to the docker container,
installs all the dependencies using poetry and elevates the permission of the startup script

In order to create the docker image of your fastapi application, run the following command:
```
 docker build -t my-fastapi-app .
```

### Docker-compose
The boilerplate also contains a docker-compose which uses the docker image built in the above step to
start the fastapi application container. Additionally, it also starts the postgres database container.
Fastapi application's container executes the startup script which runs the migrations and starts the application.

Inorder to run the docker-compose, run the following command:
```
 docker-compose up -d
```
