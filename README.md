# Users & Items API – FastAPI Schritt für Schritt

Ein modulares, produktionsnahes Python-Backend, das zeigt, wie moderne Architekturen mit **FastAPI**, **Pydantic v2**,
**SQLAlchemy 2 (Async)** und **PostgreSQL** aufgebaut werden – mit **drei Schnittstellen** (REST, GraphQL, Protobuf)
auf **einer** Service-Schicht und **einer** Datenbank.

> 🇬🇧 A modular, production-grade Python backend built step by step with FastAPI, Pydantic v2, SQLAlchemy 2 (async)
> and PostgreSQL – three APIs (REST, GraphQL, Protobuf) on one service layer and one database.

Das Repo begleitet die Videoreihe **„FastAPI Schritt für Schritt“** (60-Sekunden-Folgen, DE + EN, YouTube @MarcKronberg).
**Jede Folge ist ein Git-Tag** – der Stand *nach* der Folge:

```bash
git clone https://github.com/krocon/python-fastapi-pydantic-sqlalchemy-postgresql-demo.git
cd python-fastapi-pydantic-sqlalchemy-postgresql-demo
git checkout ep-005        # Stand nach Folge 5
```

## Voraussetzungen

- [uv](https://docs.astral.sh/uv/) (installiert auch Python 3.13 automatisch)
- ab Folge 009: Docker mit Compose v2 (`docker compose`)

## Folgen

| Folge | Tag | Thema | Topic (EN) |
|---|---|---|---|
| 001 ✅ | `ep-001` | Ein Backend, drei Schnittstellen | One backend, three APIs |
| 002 ✅ | `ep-002` | Swagger-Doku gratis | Free Swagger docs |
| 003 | `ep-003` | Projektstruktur in Schichten | A layered project structure |
| 004 | `ep-004` | Konfiguration mit pydantic-settings | Configuration with pydantic-settings |
| 005 | `ep-005` | Requests validieren mit Pydantic | Validate requests with Pydantic |
| 006 | `ep-006` | Response-Modelle | Response models |
| 007 | `ep-007` | Eigene Validatoren und EmailStr | Custom validators and EmailStr |
| 008 | `ep-008` | PATCH richtig mit exclude_unset | PATCH done right with exclude_unset |
| 009 | `ep-009` | PostgreSQL mit Docker Compose | PostgreSQL with Docker Compose |
| 010 | `ep-010` | Async Engine und Session | Async engine and session |
| 011 | `ep-011` | Tabellen als Klassen mit Mapped | Tables as classes with Mapped |
| 012 | `ep-012` | Geld nie als float speichern | Never store money as float |
| 013 | `ep-013` | 1-zu-n-Beziehungen | One-to-many relationships |
| 014 | `ep-014` | Eine Session pro Request | One session per request |
| 015 | `ep-015` | Abfragen im 2.0-Stil | Queries in 2.0 style |
| 016 | `ep-016` | flush, commit und refresh | flush, commit and refresh |
| 017 | `ep-017` | Lazy Loading und MissingGreenlet | Lazy loading and MissingGreenlet |
| 018 | `ep-018` | Migrationen mit Alembic | Migrations with Alembic |
| 019 | `ep-019` | HTTP-Statuscodes richtig setzen | Getting HTTP status codes right |
| 020 | `ep-020` | Duplikate als 409 statt 500 | Duplicates as 409, not 500 |
| 021 | `ep-021` | Pagination mit validierten Query-Parametern | Pagination with validated query parameters |
| 022 | `ep-022` | GraphQL mit Strawberry | GraphQL with Strawberry |
| 023 | `ep-023` | GraphQL-Mutations | GraphQL mutations |
| 024 | `ep-024` | Protobuf-Schema und Codegen | Protobuf schema and codegen |
| 025 | `ep-025` | Protobuf über HTTP | Protobuf over HTTP |
| 026 | `ep-026` | Tests mit pytest und httpx | Tests with pytest and httpx |
| 027 | `ep-027` | Tests gegen echtes PostgreSQL | Tests against real PostgreSQL |
| 028 | `ep-028` | Lifespan und Health-Check | Lifespan and health check |
| 029 | `ep-029` | Die API im Docker-Image | The API in a Docker image |
| 030 | `ep-030` | Finale – REST, GraphQL oder Protobuf | Finale – REST, GraphQL or Protobuf? |

---

# Schritt für Schritt

Jeder Abschnitt zeigt die Befehle zum Nachmachen für den jeweiligen Tag.

## Folge 001 – Ein Backend, drei Schnittstellen

Ziel der Reihe: REST, GraphQL und Protobuf auf einer Service-Schicht und einer PostgreSQL-Datenbank.
Start: ein FastAPI-Projekt mit uv und genau einem Endpunkt.

```bash
git checkout ep-001
uv sync                      # legt .venv an, installiert fastapi[standard]
uv run fastapi dev           # Entrypoint steht in pyproject.toml → [tool.fastapi]
curl localhost:8000/         # {"status":"online"}
```

## Folge 002 – Swagger-Doku gratis

Typ-Hinweise sind Validierung **und** Doku: `user_id: int` erscheint als Integer-Parameter in OpenAPI.

```bash
git checkout ep-002
uv run fastapi dev
curl localhost:8000/users/1      # {"id":1,"username":"alice"}
curl localhost:8000/users/abc    # 422 – int_parsing
curl localhost:8000/users/9      # 404 – User not found
# Browser: http://localhost:8000/docs (Swagger UI) · /redoc · /openapi.json
```
