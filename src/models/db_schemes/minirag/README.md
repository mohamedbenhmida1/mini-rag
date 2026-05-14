# Alembic Configuration

This folder contains the Alembic migration setup for the `minirag` PostgreSQL database.

## Files

- `alembic.ini`: Local Alembic configuration used on your machine.
- `alembic.example.ini`: Example configuration template for teammates or new environments.
- `alembic/`: Migration environment and generated revision files.

## Current Local Database URL

The local Alembic config currently points to:

```ini
postgresql://postgres:Password@localhost:5433/database_name
```

This means:

- host: `localhost`
- port: `5433`
- user: `postgres`
- password: ``
- database: ``

## When To Edit `alembic.ini`

Update `alembic.ini` when:

- the PostgreSQL host changes
- the exposed Docker port changes
- the database name changes
- the username or password changes

The main setting to update is:

```ini
sqlalchemy.url = postgresql://postgres::password@localhost:5433/database_name
```

## Why `alembic.example.ini` Exists

`alembic.example.ini` is a safe template that can be committed and shared without depending on one developer's local setup.

Recommended workflow:

1. Copy `alembic.example.ini` to `alembic.ini`.
2. Replace the placeholder values with your local database settings.
3. Run Alembic commands normally.

## Common Commands

Run these commands from this directory:

```bash
alembic current
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

## Notes

- `alembic revision --autogenerate` creates a new migration file from model changes.
- `alembic upgrade head` applies existing migrations to the database.
- If DBeaver does not show the tables, verify that it is connected to the `minirag` database, not the default `postgres` database.
