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
| 014 ✅ | `ep-014` | Eine Session pro Request | One session per request |
| 015 ✅ | `ep-015` | Abfragen im 2.0-Stil | Queries in 2.0 style |
| 016 ✅ | `ep-016` | flush, commit und refresh | flush, commit and refresh |
| 017 ✅ | `ep-017` | Lazy Loading und MissingGreenlet | Lazy loading and MissingGreenlet |
| 018 ✅ | `ep-018` | Migrationen mit Alembic | Migrations with Alembic |
| 019 ✅ | `ep-019` | HTTP-Statuscodes richtig setzen | Getting HTTP status codes right |
| 020 ✅ | `ep-020` | Duplikate als 409 statt 500 | Duplicates as 409, not 500 |
| 021 ✅ | `ep-021` | Pagination mit validierten Query-Parametern | Pagination with validated query parameters |
| 022 ✅ | `ep-022` | GraphQL mit Strawberry | GraphQL with Strawberry |
| 023 ✅ | `ep-023` | GraphQL-Mutations | GraphQL mutations |
| 024 ✅ | `ep-024` | Protobuf-Schema und Codegen | Protobuf schema and codegen |
| 025 ✅ | `ep-025` | Protobuf über HTTP | Protobuf over HTTP |
| 026 ✅ | `ep-026` | Tests mit pytest und httpx | Tests with pytest and httpx |
| 027 ✅ | `ep-027` | Tests gegen echtes PostgreSQL | Tests against real PostgreSQL |
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

## Folge 014 – Eine Session pro Request

`get_session()` ist eine Dependency mit `yield`: Session auf, Endpoint läuft, `commit` – bei einer Exception `rollback`.
`SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]` – einmal definiert, überall als Typ nutzbar.
`scope="function"` sorgt dafür, dass der Commit **vor** dem Senden der Antwort passiert (Standard wäre danach).
Die Services sind jetzt `async` und bekommen die Session als Parameter; die In-Memory-Liste ist weg.

```bash
git checkout ep-014
docker compose up -d
docker compose exec db psql -U app -d app -c "drop table if exists items, users"
uv run python -m scripts.create_tables
uv run fastapi dev
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com"}'
curl -X POST localhost:8000/api/v1/items -H "Content-Type: application/json" -d '{"title":"Keyboard","price":"49.90","owner_id":1}'
# Server neu starten – die Daten sind noch da
```

## Folge 015 – Abfragen im 2.0-Stil

`select(User).where(...).order_by(...)` baut die Abfrage, `session.scalars(stmt).all()` liefert Objekte,
`scalar_one_or_none()` genau eins oder `None`. Bedingungen lassen sich Schritt für Schritt anhängen.
Werte landen als gebundene Parameter (`$1`) in der Abfrage – keine SQL-Injection.

```bash
git checkout ep-015
uv run fastapi dev
curl "localhost:8000/api/v1/users?q=ali"          # alice, alina
curl "localhost:8000/api/v1/users?active=false"
curl localhost:8000/api/v1/users/1/items          # sortiert nach Preis, absteigend
```

## Folge 016 – flush, commit und refresh

- `flush()` schickt das SQL **jetzt** (Transaktion bleibt offen) – danach gibt es die `id`.
- `commit()` macht die Transaktion dauerhaft (bei uns in `get_session`).
- `refresh()` lädt Werte neu, die die **Datenbank** berechnet hat.

Beim INSERT holt SQLAlchemy 2 Server-Defaults wie `created_at` schon per `RETURNING` – ein `refresh` wäre ein überflüssiges SELECT.
Beim UPDATE mit `onupdate=func.now()` dagegen ist `updated_at` danach abgelaufen: ohne `refresh` endet der Zugriff im
Async-Code mit `MissingGreenlet`.

```bash
git checkout ep-016
docker compose exec db psql -U app -d app -c "drop table if exists items, users"   # neue Spalte updated_at
uv run python -m scripts.create_tables
DEBUG=true uv run fastapi dev            # SQL im Log: INSERT … RETURNING users.id, users.created_at
```

## Folge 017 – Lazy Loading und MissingGreenlet

`GET /api/v1/users/{id}` liefert jetzt den User **mit** Items. Ohne Vorkehrung will SQLAlchemy `user.items` beim Zugriff
nachladen – im Async-Code geht das nicht: `MissingGreenlet` → 500.
Lösung: `selectinload(User.items)` lädt die Items vorab mit **einer** zusätzlichen Abfrage (`WHERE owner_id IN (…)`).
`lazy="raise"` am Relationship macht jedes vergessene Nachladen sofort sichtbar.

```bash
git checkout ep-017
docker compose exec db psql -U app -d app -c "drop table if exists items, users"
uv run python -m scripts.create_tables && uv run python -m scripts.seed
DEBUG=true uv run fastapi dev
curl localhost:8000/api/v1/users/1       # User inkl. items, zwei SELECTs im Log
```

## Folge 018 – Migrationen mit Alembic

Schluss mit `create_all` und „Tabellen droppen“: Alembic versioniert das Schema.
`alembic init -t async migrations` erzeugt eine Async-Vorlage; in `migrations/env.py` kommen die URL aus den Settings
und `Base.metadata` (für `--autogenerate`). Die Naming Convention aus Folge 011 sorgt für stabile Constraint-Namen.

```bash
git checkout ep-018
docker compose exec db psql -U app -d app -c "drop table if exists items, users"   # einmalig: Altbestand weg
uv run alembic upgrade head          # Running upgrade  -> 8647569b0d13, create users and items
uv run alembic current               # 8647569b0d13 (head)
# Später, nach einer Modell-Änderung:
uv run alembic revision --autogenerate -m "add phone to users"
uv run alembic upgrade head
```

## Folge 019 – HTTP-Statuscodes richtig setzen

- `201 Created` + `Location`-Header beim Anlegen
- `204 No Content` beim Löschen (kein Body)
- `404 Not Found`, wenn es die Ressource nicht gibt – dokumentiert per `responses=`
- `422` bei ungültigen Daten kommt automatisch von FastAPI
- Konstanten aus `fastapi.status` statt magischer Zahlen

```bash
git checkout ep-019
uv run alembic upgrade head && uv run fastapi dev
curl -i -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com"}'
curl -i -X DELETE localhost:8000/api/v1/users/1      # 204
curl -i -X DELETE localhost:8000/api/v1/users/1      # 404
```

## Folge 020 – Duplikate als 409 statt 500

Ein doppelter Username löst in PostgreSQL eine `UNIQUE`-Verletzung aus → `IntegrityError` → ohne Handler **500**.
`app/core/errors.py` registriert einen Exception-Handler: Constraint-Name (dank Naming Convention) → verständliche
Meldung mit **409 Conflict**. Kein „erst SELECT, dann INSERT“ – das hätte eine Race Condition; die Datenbank entscheidet.

```bash
git checkout ep-020
uv run fastapi dev
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" -d '{"username":"bob","email":"bob@example.com"}'   # 201
curl -X POST localhost:8000/api/v1/users -H "Content-Type: application/json" -d '{"username":"bob","email":"bob2@example.com"}'  # 409 Username already exists
```

## Folge 021 – Pagination mit validierten Query-Parametern

`Limit = Annotated[int, Query(ge=1, le=100)]` und `Offset = Annotated[int, Query(ge=0)]` – einmal definiert, überall nutzbar.
`?limit=1000` wird mit 422 abgelehnt, statt die Datenbank zu fluten. Die Antwort ist ein generisches
Pydantic-Modell `Page[T]` mit `items`, `total`, `limit`, `offset` (Python-3.12-Syntax `class Page[T](BaseModel)`).
Wichtig: Pagination nur mit fester Sortierung (`order_by`), sonst springen Zeilen zwischen den Seiten.

```bash
git checkout ep-021
uv run fastapi dev
curl "localhost:8000/api/v1/users?limit=2&offset=40"
curl "localhost:8000/api/v1/users?limit=1000"        # 422 less_than_equal
```

## Folge 022 – GraphQL mit Strawberry

Zweite Schnittstelle, **gleiche** Services: `app/graphql/` definiert Typen (`@strawberry.type`) und eine `Query`.
`GraphQLRouter` hängt unter `/graphql` (im Browser: GraphiQL). Die Session kommt über denselben `SessionDep` in den Kontext.
Der Client wählt die Felder selbst – kein Over- oder Underfetching. Unbekannte Felder (`password`) lehnt das Schema ab.

```bash
git checkout ep-022
uv sync && uv run fastapi dev
curl localhost:8000/graphql -H "Content-Type: application/json" \
     -d '{"query":"{ users { username items { title price } } }"}'
# Browser: http://localhost:8000/graphql
```

## Folge 023 – GraphQL-Mutations

`@strawberry.input` beschreibt die Eingaben, `class Mutation` die schreibenden Operationen.
Validiert wird mit **denselben** Pydantic-Modellen wie bei REST (`UserCreate`, `ItemCreate`) – eine Quelle der Wahrheit.
Fehler kommen als GraphQL-`errors` mit `extensions.code` (`BAD_USER_INPUT`, `CONFLICT`, `NOT_FOUND`).

```bash
git checkout ep-023
uv run fastapi dev
# im GraphiQL-Explorer (http://localhost:8000/graphql):
mutation { createUser(input: {username: "carol", email: "carol@example.com"}) { id username role } }
mutation { createItem(input: {title: "Headset", price: "79.00", ownerId: 3}) { id title price } }
```

## Folge 024 – Protobuf-Schema und Codegen

Dritte Schnittstelle, Teil 1: der Vertrag. `app/proto/users.proto` beschreibt die Nachrichten mit **Feldnummern** –
sie, nicht die Namen, landen im Binärformat. Preise als `string` (Dezimaltext), nie als `double`.
`grpcio-tools` (nur Dev-Abhängigkeit) erzeugt `users_pb2.py` und Typ-Stubs `users_pb2.pyi`; zur Laufzeit reicht `protobuf`.

```bash
git checkout ep-024
uv sync
uv run python -m scripts.gen_proto      # = protoc -Iapp/proto --python_out=… --pyi_out=… users.proto
uv run python -c "from app.proto import users_pb2; u = users_pb2.User(id=1, username='alice'); print(u.SerializeToString())"
```

## Folge 025 – Protobuf über HTTP

`app/routers/proto.py`: gleiche Services, aber Binär rein und raus (`Content-Type: application/x-protobuf`).
Rohe Bytes per `await request.body()`, Parsen mit `CreateUserRequest.FromString(...)`, prüfen mit **demselben** `UserCreate`,
Antwort per `SerializeToString()`. Falscher Content-Type → `415`, kaputte Bytes → `422`.

Gemessen (20 User, 54 Items, gleiche Felder): JSON **5967 Bytes**, Protobuf **1944 Bytes** (≈ ein Drittel).
Mit gzip schrumpft der Abstand: 652 vs. 529 Bytes.

```bash
git checkout ep-025
uv run fastapi dev
uv run python -c "
import httpx; from app.proto import users_pb2
req = users_pb2.CreateUserRequest(username='dave', email='dave@example.com')
r = httpx.post('http://localhost:8000/api/v1/proto/users', content=req.SerializeToString(),
               headers={'Content-Type': 'application/x-protobuf'})
print(r.status_code, users_pb2.User.FromString(r.content))"
```

## Folge 026 – Tests mit pytest und httpx

`httpx.AsyncClient` mit `ASGITransport(app=app)` ruft die App **direkt** auf – kein Server, kein Port.
`pytest-asyncio` im Modus `auto` (in `pyproject.toml`) macht aus jeder `async def test_…` einen Test,
eine gemeinsame Event-Loop für alle Tests hält den Connection-Pool stabil.
Noch ein Haken: Die Tests schreiben in die Entwicklungs-Datenbank – das lösen wir in Folge 027.

```bash
git checkout ep-026
docker compose up -d && uv run alembic upgrade head
uv run pytest -v          # 4 passed
```

## Folge 027 – Tests gegen echtes PostgreSQL

Kein SQLite-Ersatz: Die Tests laufen gegen PostgreSQL – in einer **eigenen** Datenbank `app_test`.
1. Session-Fixture legt `app_test` neu an und baut das Schema mit **Alembic** (`command.upgrade`) – die Migrationen werden mitgetestet.
2. Jeder Test läuft in einer äußeren Transaktion, die am Ende **zurückgerollt** wird (`join_transaction_mode="create_savepoint"`).
3. `app.dependency_overrides[get_session]` tauscht die Session aus – für REST, GraphQL und Protobuf zugleich.

```bash
git checkout ep-027
docker compose up -d
uv run pytest -v         # 14 passed – und die Entwicklungs-Datenbank bleibt unberührt
```
