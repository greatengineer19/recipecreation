# FastAPI Starter

Production-ready FastAPI REST API with PostgreSQL, structured for Neon + Railway deployment.

## Project Structure

```
app/  
├── api/v1/
│   ├── endpoints/items.py   # Route handlers
│   └── router.py            # Route aggregator
├── core/
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # SQLAlchemy engine + get_db dependency
│   ├── error_handlers.py    # Global FastAPI exception handlers
│   ├── exceptions.py        # Domain exceptions
│   └── responses.py         # Unified response envelope
├── models/
│   └── item.py              # SQLAlchemy ORM models
├── repositories/
│   └── item_repository.py   # DB access layer
├── schemas/
│   └── item.py              # Pydantic request/response schemas
├── services/
│   └── item_service.py      # Business logic
└── main.py                  # App factory
migrations/                  # Alembic
tests/
├── conftest.py              # Fixtures (SQLite in-memory)
└── test_items.py            # CRUD test suite
```

## Quick Start (Local)

```bash
# 1. Clone & install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit DATABASE_URL for your local Postgres

# 3. Run migrations
alembic upgrade head

# 4. Start dev server
uvicorn app.main:app --reload

# Docs → http://localhost:8000/docs
```

## Running Tests

Tests use **SQLite in-memory** — no Postgres needed.

```bash
pytest                        # all tests
pytest -v --tb=short          # verbose
pytest --cov=app tests/       # with coverage
```

## Deploy to Railway + Neon

### 1. Neon (Postgres)
1. Create a project at [neon.tech](https://neon.tech)
2. Copy the connection string: `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require`

### 2. Railway
1. Push this repo to GitHub
2. New project → Deploy from GitHub
3. Add env var: `DATABASE_URL=<neon connection string>`
4. Railway auto-detects the `Procfile`:
   - `release` command runs `alembic upgrade head`
   - `web` command starts uvicorn on `$PORT`

That's it — Railway handles TLS, `$PORT`, and zero-downtime deploys.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /api/v1/items/ | List (paginated) |
| POST | /api/v1/items/ | Create |
| GET | /api/v1/items/{id} | Get by ID |
| PATCH | /api/v1/items/{id} | Partial update |
| DELETE | /api/v1/items/{id} | Delete |

## Response Shape

**Success**
```json
{ "success": true, "message": "OK", "data": { ... } }
```

**Paginated**
```json
{ "success": true, "data": [...], "total": 42, "page": 1, "page_size": 20 }
```

**Error**
```json
{ "success": false, "message": "Item with id=99 not found.", "detail": null }
```
