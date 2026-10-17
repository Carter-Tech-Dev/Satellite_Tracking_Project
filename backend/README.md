# Backend Creation

## Development Environment

Create a virtual environment and then activate it using the following:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

This will ensure libraries installed for this project don't affect the system's global settings.

## Testing

Pytest is used in this project with the following plugins.

```bash
pip install -U pytest pytest-cov pytest-xdist
```

To run test coverage:

```bash
python3 -m pytest --cov-report=term-missing --cov
```

## Creating the Database

```bash
pip install asyncpg asyncio python-dotenv
```

To create and seed the database:

```bash
python3 db_seed.py
```

## Creating the Server

```bash
pip3 install "fastapi[standard]" pydantic
```

## Running the Server

```bash
fastapi dev
```

## Server Documentation

There are two popular types of documentation used with FastAPI.
1. `/docs`
2. `/redoc`

The `/docs` endpoint is powered by Swagger UI and features an interactive playground to test endpoints directly from the browser and `/redoc` is powered by ReDoc and focuses on delivering a clean, highly readable, and structured three-paneled layout optimized for reference and technical sharing.

## Utils Folder

### Celestrak

