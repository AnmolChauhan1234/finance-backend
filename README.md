# 💼 Finance Dashboard Backend

> A clean, scalable backend system for managing financial records with role-based access control and analytics.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Roles and Access Control](#roles-and-access-control)
- [API Overview](#api-overview)
- [Features](#features)
- [Soft Delete](#soft-delete)
- [Setup Instructions](#setup-instructions)
- [Cross-Platform Compatibility](#cross-platform-compatibility)
- [Authentication](#authentication)
- [Testing](#testing)
- [Trade-offs Considered](#trade-offs-considered)
- [Assumptions](#assumptions)
- [What Was Built](#what-was-built)

---

## Overview

This project is a backend service for a **finance dashboard** where users interact with financial records based on their assigned roles. It demonstrates strong backend architecture, clear separation of concerns, and reliable data handling.

**Core capabilities:**

- User management with role-based access
- Financial record CRUD operations with soft delete
- Dashboard analytics (income, expenses, trends)
- JWT-based authentication
- Input validation and meaningful error handling

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| Containerization | Docker |
| Testing | pytest |

---

## Architecture

The system follows a strict **layered architecture** to ensure clean separation of concerns:

```
Request → Controller (API) → Service (Business Logic) → Repository (DB Access) → Database
```

```
app/
├── api/            # Routes & dependency injection
├── core/           # Config & security utilities
├── db/             # Database setup & session management
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic request/response schemas
├── repositories/   # Database access layer
└── services/       # Business logic layer
```

**Key design decisions:**

- **Dependency Injection** via `FastAPI Depends` for testability and modularity
- **Enum normalization** — accepts `"ADMIN"` and `"admin"` interchangeably, with strict internal validation
- **Database-first migrations** via Alembic for consistent schema management
- **Soft delete** enforced at the repository layer so no deleted record leaks into any query

---

## Roles and Access Control

Access control is enforced at the API level using dependency-based guards.

| Role | Permissions |
|---|---|
| `Viewer` | View dashboard data |
| `Analyst` | View records + analytics |
| `Admin` | Full access — CRUD on users & records, restore deleted records |

---

## API Overview

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate and receive a JWT token |

### Users *(Admin only)*

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/users` | Create a new user |
| `GET` | `/api/v1/users` | List all users |

### Financial Records

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/records` | Create a financial record |
| `GET` | `/api/v1/records` | Get active records (filter by `type`, `category`, `date`) |
| `PUT` | `/api/v1/records/{id}` | Update a record |
| `DELETE` | `/api/v1/records/{id}` | Soft delete a record |
| `POST` | `/api/v1/records/{id}/restore` | Restore a soft-deleted record |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/dashboard/summary` | Full financial summary (excludes soft-deleted records) |

The dashboard summary includes:
- Total income & total expenses
- Net balance
- Category-wise totals
- Monthly trends
- Recent activity

> Interactive API docs available at `http://localhost:8000/docs` after startup.

---

## Features

### 1. User Management
- Create users and assign roles (`Viewer`, `Analyst`, `Admin`)
- Activate / deactivate users
- Secure JWT-based authentication

### 2. Financial Records
- Full CRUD support with soft delete
- Filter by type (`income` / `expense`), category, and date — exact match filtering; `ILIKE` fuzzy search is a planned enhancement
- Input validation: amount must be > 0, all fields strongly typed

### 3. Dashboard Analytics
- Total income, total expenses, net balance
- Category-wise breakdown
- Monthly trends
- Recent activity feed
- Soft-deleted records are automatically excluded from all analytics

### 4. Validation and Error Handling
- Schema validation via **Pydantic**
- Meaningful HTTP status codes (`400`, `401`, `403`, `404`, `422`)
- Enum normalization for resilient client integration

---

## Soft Delete

This project implements **proper soft delete** — not just an `is_deleted` flag, but a fully enforced pattern across all layers.

### What was implemented

| Concern | Implementation |
|---|---|
| Model flag | `is_deleted` boolean + `deleted_at` timestamp on the record model |
| Query enforcement | All repository queries filter `is_deleted = false` by default |
| Delete endpoint | Sets `is_deleted = true` and records `deleted_at` — no row is ever removed |
| Restore endpoint | `POST /api/v1/records/{id}/restore` reactivates a soft-deleted record |
| Analytics integrity | Dashboard summary excludes soft-deleted records automatically |
| Data integrity | Deleted data is preserved in the database for auditing and recovery |

### Why this matters

A naive implementation just adds a column and forgets about it. This implementation:

- Enforces the filter at the **repository layer**, so no query can accidentally return deleted records
- Handles the **delete and restore lifecycle** explicitly, not as an afterthought
- Keeps **data integrity intact** — nothing is ever permanently lost
- Makes the system **audit-friendly** — you always know what was deleted and when

---

## Setup Instructions

### Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose installed

### 1. Clone the Repository

```bash
git clone https://github.com/AnmolChauhan1234/finance-backend.git
cd finance-backend
```

### 2. Start Services

```bash
docker-compose up --build
```

### 3. Database Migrations

Migrations run **automatically** on startup via the container entrypoint. No manual step required.

### 4. Access the API

```
http://localhost:8000/docs
```

---

## Cross-Platform Compatibility

This project enforces Unix (LF) line endings via `.gitattributes` to ensure consistent behaviour across Mac, Linux, and Windows — particularly important for Docker execution where Windows-style (CRLF) line endings can cause shell script failures inside containers.

---

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

**Login endpoint:**

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "adminpassword"
}
```

A default **admin user** is seeded on first startup with the credentials above.

> **Note:** The login endpoint uses `OAuth2PasswordRequestForm`, which requires a field named `username`. In this project, the `username` field accepts the user's **email address**.

---

## Testing

Unit tests are written with **pytest** and cover authentication, user management, record operations, and dashboard analytics.

**Run tests inside Docker:**

```bash
docker-compose exec backend pytest -v
```

Test coverage includes:
- Authentication flow
- User creation & listing
- Record CRUD operations
- Soft delete and restore behaviour
- Dashboard summary endpoint

---

## Trade-offs Considered

| Decision | Choice Made | Rationale |
|---|---|---|
| Simplicity vs Scalability | Layered monolith | Keeps the system readable and suitable for assignment scope; structured for future microservice extraction |
| On-demand Analytics vs Performance | Calculated at request time | Simple to implement; Redis caching can be added in production for scale |
| Flexible Input vs Strict Validation | Enum normalization (`"ADMIN"` to `"admin"`) | Makes the API resilient to inconsistent client inputs while enforcing strict internal contracts |
| Monolith vs Distributed | Monolith with clean service/repository separation | Clear boundaries make it straightforward to split into microservices later if needed |
| Hard Delete vs Soft Delete | Soft delete with restore support | Preserves data integrity and audit history; no record is ever permanently lost |

---

## Assumptions

- Authentication is simplified using stateless JWT (no refresh token rotation)
- Financial data is scoped per user — users only access their own records
- No external third-party integrations (focused on core backend logic)
- Pagination uses offset-based `skip`/`limit` — sufficient for this scope but can be upgraded to cursor-based for large datasets

---

## What Was Built

This project fulfills all core assignment requirements and goes beyond them with several optional enhancements.

### Core Requirements — All Completed

- [x] User management with role assignment and active/inactive status
- [x] Financial records CRUD with filtering by type, category, and date
- [x] Dashboard summary APIs — income, expenses, net balance, category totals, monthly trends
- [x] Role-based access control enforced at the API level (Viewer / Analyst / Admin)
- [x] Input validation and structured error handling (Pydantic + HTTP status codes)
- [x] Data persistence with PostgreSQL and Alembic migrations

### Optional Enhancements — Also Completed

- [x] JWT-based authentication with seeded admin user
- [x] Soft delete with full restore support (`deleted_at` timestamp, enforced in all queries)
- [x] Offset-based pagination (`skip` / `limit`) on record listing
- [x] Unit tests with pytest covering auth, users, records, and dashboard
- [x] Auto-generated API documentation (Swagger UI at `/docs`, ReDoc at `/redoc`)
- [x] Dockerized setup with single-command startup

### Further Improvements Possible

These are production-scale additions beyond the assignment scope that could be added if needed:

- Cursor-based pagination for better performance on large datasets
- Full-text / fuzzy search — basic filtering by `type`, `category`, and `date` is implemented; `ILIKE` search across `notes` and fuzzy category matching is not yet added
- Redis caching for dashboard analytics
- JWT refresh token rotation
- CI/CD pipeline and cloud deployment (AWS / Render)

---

## Author

**Anmol Chauhan** — Backend Developer Intern Candidate

> This project was built as part of an assignment to demonstrate backend engineering skills, system design thinking, and implementation quality.
