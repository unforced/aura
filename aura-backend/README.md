# Aura Backend

This is the FastAPI application that serves as the backend for Project Aura.

## Setup and Development

### 1. Prerequisites
- Python 3.9+
- [Docker](https://www.docker.com/) and Docker Compose
- An active Python virtual environment.

### 2. Environment Configuration
The application requires a set of environment variables to run.

- Copy the example environment file:
  ```bash
  cp .env.example .env
  ```
- Review the `.env` file. The default values should work for a local setup, but you can customize them if needed. The `SECRET_KEY` is particularly important for JWT security.

### 3. Install Dependencies
Install the required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Set Up Databases
The application requires a PostgreSQL database. We use Docker to run a container.

- **Start PostgreSQL Container:**
  ```bash
  docker run -d --name aura-postgres -e POSTGRES_USER=aurauser -e POSTGRES_PASSWORD=aurapass -e POSTGRES_DB=aura_dev -p 5432:5432 -v aura-pgdata:/var/lib/postgresql/data postgres:15
  ```
- **Apply Database Migrations:**
  This command creates the necessary tables (`users`, `documents`, etc.) in the database.
  ```bash
  alembic upgrade head
  ```

### 5. Run the Application
Use `uvicorn` to run the FastAPI development server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## Testing
The application includes a test suite using `pytest`.

### 1. Test Database Setup
- Create a test database for isolated testing:
  ```bash
  # Ensure the PostgreSQL container is running
  docker exec aura-postgres createdb -U aurauser aura_test
  ```
- Create a `.env.test` file for test-specific environment variables:
  ```bash
  echo "DATABASE_URL=postgresql://aurauser:aurapass@localhost:5432/aura_test" > .env.test
  ```

### 2. Run Tests
Execute the test suite with `pytest`:
```bash
pytest
``` 