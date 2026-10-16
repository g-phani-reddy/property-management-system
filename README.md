# Property Management API

A Django REST Framework API for staff to manage properties, units, tenants, and
time-bounded rental contracts.

## Requirements

- Python 3.10+
- PostgreSQL 13+

## Run locally with PostgreSQL

Install the dependencies, create a PostgreSQL database and user, and put the
connection settings in a `.env` file in the project root:

```dotenv
POSTGRES_DB=property_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`. Set `SECRET_KEY` and
`DEBUG=false` outside local development.

Resource IDs are UUIDs.

## Run with Docker Compose

Create a `.env` file in the project root with PostgreSQL credentials and a
strong Django secret:

```dotenv
POSTGRES_DB=property_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change-this-password
SECRET_KEY=change-this-to-a-long-random-secret
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1
```

Build and start the API and PostgreSQL:

```sh
docker compose up --build
```

The API is available at `http://127.0.0.1:8000/api/`. Compose waits for
PostgreSQL to become healthy, applies migrations when the API container starts,
and stores database data in a persistent named volume. Stop the services with
`docker compose down`; database data remains in the volume. To delete the
database data as well, run `docker compose down --volumes`.

## Authentication

Register a staff user:

```sh
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"staff@example.com","password":"StrongPass123","first_name":"Sam"}'
```

Log in to receive an access and refresh token:

```sh
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"staff@example.com","password":"StrongPass123"}'
```

Send the returned access token on protected requests:

```sh
curl http://127.0.0.1:8000/api/properties \
  -H 'Authorization: Bearer <access-token>'
```

Refresh an access token with `POST /api/auth/refresh` and
`{"refresh":"<refresh-token>"}`.

## Endpoints

See the [API reference](./docs/API.md) for request and response fields, examples,
authentication requirements, and validation behavior for every endpoint.

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/auth/register` | Register a staff user |
| POST | `/api/auth/login` | Obtain JWT access and refresh tokens |
| POST | `/api/auth/refresh` | Refresh an access token |
| GET, PUT, PATCH | `/api/auth/me` | Retrieve or edit the authenticated user's profile |
| POST, GET | `/api/properties` | Create and list properties |
| GET, PUT, PATCH | `/api/properties/{property_id}` | Retrieve or edit a property and its units |
| POST | `/api/properties/{property_id}/units` | Add a unit to a property |
| GET | `/api/units?status=available` | List units; filter by `available` or `occupied` |
| GET, PUT, PATCH | `/api/units/{unit_id}` | Retrieve or edit a unit |
| POST, GET | `/api/members` | Create and list members |
| POST, GET | `/api/contracts` | Create and list contracts |
| GET | `/api/contracts?active=true` | List contracts active today |

For `active`, use `true` for contracts active today or `false` for contracts
that are not active today. Contracts are active when today's date falls
inclusively between their start and end dates.

## Contract rules

- A contract end date must be on or after its start date.
- A unit cannot have two contracts whose inclusive date ranges overlap.
- If omitted, contract monthly rent is copied from the unit at creation time.
- Total value is the monthly rent times the number of monthly billing periods.
  A partial period is charged as a full period; dates on monthly anniversaries
  count as one period. For example, January 15 through February 14 is one
  period, while January 15 through February 15 is one period.
- A unit is `occupied` when at least one contract for it is active today;
  otherwise it is `available`. Future contracts do not occupy a unit early.
- Contract creation locks the unit within a database transaction before
  checking for overlaps, preventing concurrent bookings on PostgreSQL.

## Example responses

A successful `POST /api/properties` response:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Central Apartments",
  "address": "1 Main Street",
  "units": [],
  "created_at": "2026-10-15T14:00:00Z"
}
```

A successful `POST /api/contracts` response (when monthly rent is omitted):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "unit": "550e8400-e29b-41d4-a716-446655440002",
  "member": "550e8400-e29b-41d4-a716-446655440003",
  "start_date": "2026-10-15",
  "end_date": "2027-10-14",
  "monthly_rent": "1200.00",
  "total_value": "14400.00",
  "created_at": "2026-10-15T14:00:00Z"
}
```

## Run tests

```sh
python manage.py test
```
