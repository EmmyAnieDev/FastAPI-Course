# INTRODUCTION TO FASTAPI

## INSTALLATION OF PYTHON, VIRTUAL ENVIRONMENT, AND FASTAPI

### Create a virtual environment 

```commandline
python3 -m venv env
```

### Activate Virtual environment

- On macOS/Linux:
    ```commandline
    source env/bin/activate
    ```

- On Windows (Command Prompt):
    ```commandline
    env\Scripts\activate
    ```
  
- On Windows (PowerShell):
    ```commandline
    env\Scripts\Activate.ps1
    ```

### Install FastAPI

```commandline
pip install fastapi
```

## FastAPI Project Architecture

```bash
myapp/
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   ├── env.py                # Alembic environment settings
│   ├── script.py.mako        # Template for migrations
│   └── README                # Documentation
│
├── app/
│   ├── __init__.py
│   ├── db.py               # FastAPI app initialization
│   │
│   ├── middleware/           # Custom middleware
│   │   ├── __init__.py
│   │   ├── logging.py        # Request logging
│   │   ├── cors.py           # CORS handling
│   │   ├── error_handler.py  # Error handling
│   │   └── rate_limiter.py   # Rate limiting
│   │
│   ├── core/                 # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py         # Environment variables and configuration
│   │   ├── security.py       # Security utilities (JWT, hashing)
│   │   └── exceptions.py     # Custom exception handlers
│   │
│   ├── api/                  # API routes and dependencies
│   │   ├── __init__.py
│   │   ├── deps.py           # Dependency injection
│   │   ├── v1/               # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/    # Endpoints grouped by functionality
│   │   │   │   ├── users.py
│   │   │   │   ├── items.py
│   │   │   ├── router.py     # Route registration
│   │
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── schemas/              # Pydantic models for validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── crud/                 # CRUD operations
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── email_services.py
│   │   └── image_processing.py
│
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_items.py
│   └── test_auth.py
│
├── .env                      # Environment variables
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration for multi-container setup
├── Dockerfile                 # Docker configuration for deployment
└── README.md                  # Project documentation

```

## SERIALIZATION MODEL

- Serialization Model helps us change data from our server/database into something any client that accesses our server can understand.
- It can also be the reverse, where the client sends data to the server, and we deserialize it back into a format that our application or database can process.

## SETTING UP A DATABASE

```commandline
pip install asyncpg
pip install pydantic-settings
pip install sqlmodel
```

- Create `.env` file and add your DB configurations

## Alembic

- Alembic is a database migration tool for SQLAlchemy that helps you manage and version-control changes to your database schema. 
- It allows you to create, modify, and roll back database tables without losing data.

```commandline
pip install alembic
```

- To create a migration environment

  ```commandline
  alembic init -t async migrations
  ```
  
  *Added: migrations/env.py line 9-14, 20 30, migrations/script.py.mako line 12*


- Migrations/Versions: This track migration or database changes at a specific point of time.

  ```commandline
  alembic revision --autogenerate -m "init"
  ```

- Apply Migration to Database

  ```commandline
  alembic upgrade head
  ```
  
## Install PASSLIB to HASH users Password

```commandline
pip install passlib
pip install bcrypt
```
  
## Install JWT

```commandline
pip install pyjwt
```
  
## Install REDIS to store revoked tokens

```commandline
pip install redis
```
  
## ROLE BASE ACCESS CONTROL (RBAC)

This allows access to a specific endpoint/function within our API/APP depending on the role the user has within our Application.

# admin
[
    "adding users",
    "change roles",
    "crud on users",
    "book submissions",
    "crud on books",
    "crud on reviews",
    "revoking access"
]

# users
[
    "crud on their own book submissions",
    "crud on their reviews",
    "crud on their own accounts"
]
  
## MIDDLEWARE

These are functions that sit between our request and our responses. Middleware can be used to check for authentication, modify headers in request or response and more before actually sending them to wherever they'll be handled.

**When a client makes a request, the `middkeware` get the request performs actions on that request and then send the request to the request handler function, which happens same way for response**