# Backend Overview

## Project Description

The backend for the Memberly application is a robust, multi-tenant FastAPI-based system designed to manage memberships efficiently. It includes features such as authentication, database management, payment processing, and communication services. The backend is built with scalability, security, and maintainability in mind.

## Key Features

### 1. Multi-Tenant Architecture

- Supports multiple tenants with schema-based isolation.
- Middleware for tenant identification and context switching.

### 2. Database Management

- PostgreSQL database with SQLAlchemy ORM.
- Alembic for database migrations.
- Connection pooling and health checks.

### 3. Authentication

- JWT-based authentication.
- Role-based access control.
- Password hashing and refresh tokens.

### 4. API Endpoints

- CRUD operations for members and memberships.
- Payment processing and transaction history.
- Communication services for email, SMS, and push notifications.

### 5. Background Tasks

- Bulk communications.
- Recurring payments.
- Report generation.

### 6. Logging and Monitoring

- Structured logging for requests, errors, and exceptions.
- Tenant-aware logging.

### 7. Documentation

- OpenAPI/Swagger integration for detailed API documentation.

## Setup Instructions

### 1. Environment Configuration

- Copy `.env.example` to `.env` and update the environment variables.
- Ensure PostgreSQL and Redis are installed and running locally.

### 2. Database Setup

- Create a PostgreSQL database and user.
- Update the `.env` file with the database credentials.
- Run Alembic migrations to set up the schema:
  ```bash
  alembic upgrade head
  ```

### 3. Running the Application

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Start the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```

### 4. Testing the API

- Access the API documentation at `http://127.0.0.1:8000/docs`.

## Folder Structure

- `app/`: Core application logic.
- `api/`: API routers and endpoints.
- `core/`: Configuration, middleware, and utilities.
- `db/`: Database connection and session management.
- `models/`: SQLAlchemy models.
- `schemas/`: Pydantic schemas.
- `services/`: Business logic and service layers.
- `utils/`: Helper functions.
- `tests/`: Test cases and fixtures.
- `alembic/`: Database migration scripts.

## Future Enhancements

- Automated testing framework.
- Advanced monitoring and analytics.
- Support for additional payment gateways.
