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
| 003 ✅ | `ep-003` | Projektstruktur in Schichten | A layered project structure |
| 004 ✅ | `ep-004` | Konfiguration mit pydantic-settings | Configuration with pydantic-settings |
| 005 ✅ | `ep-005` | Requests validieren mit Pydantic | Validate requests with Pydantic |
| 006 ✅ | `ep-006` | Response-Modelle | Response models |
| 007 ✅ | `ep-007` | Eigene Validatoren und EmailStr | Custom validators and EmailStr |
| 008 ✅ | `ep-008` | PATCH richtig mit exclude_unset | PATCH done right with exclude_unset |
| 009 ✅ | `ep-009` | PostgreSQL mit Docker Compose | PostgreSQL with Docker Compose |
| 010 ✅ | `ep-010` | Async Engine und Session | Async engine and session |
| 011 ✅ | `ep-011` | Tabellen als Klassen mit Mapped | Tables as classes with Mapped |
| 012 ✅ | `ep-012` | Geld nie als float speichern | Never store money as float |
| 013 ✅ | `ep-013` | 1-zu-n-Beziehungen | One-to-many relationships |
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

## Folge 003 – Projektstruktur in Schichten

`main.py` wandert nach `app/`. Router sprechen HTTP, Services enthalten die Logik – und wissen nichts von HTTP.

```
app/
├── main.py              # App bauen, Router einhängen
├── routers/users.py     # HTTP: Pfade, Statuscodes  (APIRouter, prefix /api/v1/users)
└── services/user_service.py   # Logik, später mit Datenbank
# kommen noch: core/ (Konfiguration, DB) · schemas/ (Pydantic) · models/ (SQLAlchemy) · graphql/ · proto/
```

```bash
git checkout ep-003
uv run fastapi dev               # Entrypoint jetzt app.main:app
curl localhost:8000/api/v1/users
```

## Folge 004 – Konfiguration mit pydantic-settings

`app/core/config.py`: eine typisierte `Settings`-Klasse. Reihenfolge: Umgebungsvariable > `.env` > Standardwert.
Falsche Werte stoppen die App **beim Start** – nicht erst beim ersten Request.

```bash
git checkout ep-004
cp .env.example .env
uv run python -c "from app.core.config import settings; print(settings)"
DEBUG=vielleicht uv run python -c "from app.core.config import settings"   # ValidationError: bool_parsing
```

## Folge 005 – Requests validieren mit Pydantic

`app/schemas/user.py`: `UserCreate` beschreibt den Request-Body. FastAPI validiert **vor** deinem Code –
ungültige Daten bekommen automatisch `422` mit einer Liste aller Fehler.

```bash
git checkout ep-005
uv run fastapi dev
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" \
     -d '{"username":"alice","email":"alice@example.com"}'          # 201
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" \
     -d '{"username":"Al","role":"superuser"}'                      # 422: string_too_short, missing, literal_error
```

## Folge 006 – Response-Modelle

`UserRead` beschreibt, was die API **zurückgibt**. Der Rückgabetyp der Funktion (`-> UserRead`) ist das Response-Modell:
FastAPI validiert, filtert auf die deklarierten Felder und dokumentiert das Schema in `/docs`.
`from_attributes=True` erlaubt, Objekte (später SQLAlchemy-Modelle) statt Dicts zurückzugeben.

```bash
git checkout ep-006
uv run fastapi dev
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" \
     -d '{"username":"alice","email":"alice@example.com"}'
# {"username":"alice","email":"alice@example.com","role":"user","id":1,"is_active":true,"created_at":"…Z"}
```

## Folge 007 – Eigene Validatoren und EmailStr

- `EmailStr` prüft echte E-Mail-Syntax (Paket `email-validator`, steckt in `fastapi[standard]`) und normalisiert die Domain.
- `@field_validator(..., mode="before")` läuft **vor** der Typprüfung (Normalisieren), ohne `mode` **danach** (Regeln).
- Ein `ValueError` im Validator wird automatisch zu `422`.

```bash
git checkout ep-007
uv run fastapi dev
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" \
     -d '{"username":"  Alice ","email":"Alice@Example.COM"}'    # 201 → "alice", "Alice@example.com"
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" \
     -d '{"username":"root","email":"root@example.com"}'          # 422 – 'root' is reserved
```

## Folge 008 – PATCH richtig mit exclude_unset

`UserUpdate`: alle Felder optional. `model_dump(exclude_unset=True)` liefert nur die Felder, die der Client
**wirklich geschickt** hat – sonst würden fehlende Felder mit `None` überschrieben.

```bash
git checkout ep-008
uv run fastapi dev
curl -X POST  localhost:8000/api/v1/users   -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com"}'
curl -X PATCH localhost:8000/api/v1/users/1 -H "Content-Type: application/json" -d '{"role":"admin"}'   # nur role ändert sich
curl -X PATCH localhost:8000/api/v1/users/1 -H "Content-Type: application/json" -d '{"email":null}'      # 422
```

## Folge 009 – PostgreSQL mit Docker Compose

`compose.yaml` startet PostgreSQL 18 mit Volume (Daten überleben Neustarts) und Healthcheck.
Ab PostgreSQL 18 wird das Volume auf `/var/lib/postgresql` gemountet (nicht mehr `…/data`).

```bash
git checkout ep-009
cp .env.example .env
docker compose up -d            # startet den Service db
docker compose ps               # STATUS: … (healthy)
docker compose exec db psql -U app -d app -c "select version();"
```

## Folge 010 – Async Engine und Session

`app/core/database.py`: **eine** Engine pro Prozess (= Connection-Pool) und eine `async_sessionmaker`-Fabrik.
Treiber `asyncpg` steckt in der URL (`postgresql+asyncpg://`). SQLAlchemy 2.1 braucht das Extra `sqlalchemy[asyncio]`
(installiert `greenlet`).

```bash
git checkout ep-010
docker compose up -d
uv sync
uv run python -m scripts.db_check      # PostgreSQL 18.x on …
DEBUG=true uv run python -m scripts.db_check   # mit SQL-Log (echo)
```

## Folge 011 – Tabellen als Klassen mit Mapped

`app/models/user.py`: Ein SQLAlchemy-2-Modell mit `Mapped[...]`. Der Python-Typ bestimmt die Spalte und `NOT NULL`
(`Mapped[str | None]` wäre nullable). `server_default=func.now()` setzt die Datenbank selbst.
Die Tabelle legt vorübergehend ein Skript an – ab Folge 018 übernimmt Alembic.

```bash
git checkout ep-011
docker compose up -d
uv run python -m scripts.create_tables      # zeigt das CREATE TABLE
docker compose exec db psql -U app -d app -c "\d users"
```

## Folge 012 – Geld nie als float speichern

`float` ist binär und rundet: `sum([19.99] * 10)` ergibt `199.89999999999998`. Für Preise daher
`Numeric(10, 2)` in der Datenbank und `Decimal` in Python und Pydantic (`max_digits`, `decimal_places`).
Pydantic gibt `Decimal` im JSON als **String** aus (`"19.99"`) – verlustfrei für jeden Client.

```bash
git checkout ep-012
uv run python -c "print(sum([19.99] * 10))"                                   # 199.89999999999998
uv run python -c "from decimal import Decimal; print(sum([Decimal('19.99')] * 10))"   # 199.90
uv run python -m scripts.create_tables                                        # items.price NUMERIC(10, 2)
```

## Folge 013 – 1-zu-n-Beziehungen

Ein User hat viele Items: `ForeignKey("users.id", ondelete="CASCADE")` auf der n-Seite,
`relationship(back_populates=…)` auf beiden Seiten. `cascade="all, delete-orphan"` + `passive_deletes=True`:
Items gehören zu ihrem User – gelöscht wird per `ON DELETE CASCADE` direkt in PostgreSQL.

```bash
git checkout ep-013
docker compose exec db psql -U app -d app -c "drop table if exists items, users"
uv run python -m scripts.create_tables
uv run python -m scripts.seed            # user 1: [(1, 'Keyboard', 1), (2, 'Mouse', 1)]
```
