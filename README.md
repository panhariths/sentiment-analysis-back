# fastapi-boilerplate

Boilerplate template for FastAPI repositories.

## Table of Contents
- [Project Structure](#Project-Structure)
- [Pre-requisites](#pre-requisites)
  - [Poetry](#poetry)
  - [Enabling pre-commit hooks](#enabling-pre-commit-hooks)
- [Connecting with database](#Connecting-with-database)
  - [Creating migrations](#creating-migrations)
- [Docker Setup](#Docker-Setup)
  - [Dockerfile](#Dockerfile)
  - [Docker-compose](#Docker-compose)
- [Contributors](#Contributors)

## Project Structure
The project structure is as follows:
```
 |-- app
 |   |-- app1
 |   |   |-- handlers
 |   |   |-- models
 |   |   |-- schemas
 |   |   |-- services
 |   |-- app2
 |   |    ...
 |   |-- routes.py
 |   |-- server.py
 |-- config
 |   |-- config.py
 |   |-- logger
 |   |   |-- logger_config.py
 |-- datastores
 |   |-- cache
 |   |-- database
 |-- migrations
 |-- tests
 |-- utils
 |    |-- dependencies.py
 |-- main.py
```

- **app**: This package contains all the fastapi applications. Each application is a package in itself and contains
  handlers, models, schemas, service. The package also contains routes.py and server.py files. routes.py contains all the
  routes of the application and server.py contains the startup script of the application.
- **config**: This package contains all the configurations of the application. config.py contains all the environment
  variables and logger_config.py contains the configuration of the logger.
- **datastores**: This package contains all the datastores of the application. Currently, it contains cache and database
  datastores. Each datastore is a package in itself and contains all the models of that datastore.
- **migrations**: This package contains all the migrations of the application. It uses alembic for migrations.
- **tests**: This package contains all the tests of the application.
- **utils**: This package contains all the utility functions of the application. Currently, it contains dependencies.py
  which contains all the dependencies of the application.
- **main.py**: This file contains the startup script of the application.


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

## Contributors
- [Sarwan Ahmed](https://github.com/Sarwan-Ahmed)
- [Sohaib Omar](https://github.com/sohaibomr)
- [Syed Farhan Ahmed](https://github.com/farhanahmed-emumba)
