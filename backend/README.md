# EventFlow Pro — Backend

## Folder Guide

| Folder       | Purpose                          |
|-------------|----------------------------------|
| `api/`      | FastAPI route handlers           |
| `agents/`   | AI agent logic                   |
| `services/` | Business logic layer             |
| `database/` | DB connection & session setup    |
| `models/`   | SQLAlchemy ORM models            |
| `schemas/`  | Pydantic request/response models |
| `utils/`    | Helper functions                 |
| `config/`   | Extra config modules             |

## Key Files

| File               | Purpose                     |
|--------------------|-----------------------------|
| `config.py`        | App settings (from `.env`)  |
| `.env.example`     | Env var template            |
| `requirements.txt` | Python dependencies         |
