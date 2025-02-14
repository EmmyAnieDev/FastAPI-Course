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
│   ├── main.py               # FastAPI app initialization
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