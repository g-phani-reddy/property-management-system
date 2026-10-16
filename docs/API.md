# Property Management API Reference

Base URL: `http://127.0.0.1:8000/api`

All resource IDs are UUIDs. Unless noted otherwise, endpoints require an
authenticated staff user. The profile endpoint requires authentication and
operates only on the current user. Send the access token as a bearer token:

```http
Authorization: Bearer <access-token>
```

Successful list endpoints return JSON arrays. Validation errors return
`400 Bad Request`; unauthenticated requests return `401 Unauthorized`, and
requests from non-staff users return `403 Forbidden`.

## Authentication

### Register a staff user

`POST /auth/register` — public.

Request:

```json
{
  "email": "staff@example.com",
  "password": "StrongPass123",
  "first_name": "Sam",
  "last_name": "Taylor"
}
```

`email` and `password` are required. Passwords must be at least 8 characters
and pass Django's configured password validators. The user is created as
staff. The response contains `id`, `email`, `first_name`, and `last_name`;
password is never returned.

### Log in

`POST /auth/login` — public.

Request:

```json
{
  "email": "staff@example.com",
  "password": "StrongPass123"
}
```

Response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Only staff users can obtain tokens. Access tokens last 30 minutes and refresh
tokens last 1 day.

### Refresh an access token

`POST /auth/refresh` — public.

Request:

```json
{
  "refresh": "<refresh-token>"
}
```

Response:

```json
{
  "access": "<new-access-token>"
}
```

### Retrieve or edit the current user's profile

`GET`, `PUT`, `PATCH /auth/me`

Returns or updates only the authenticated user's profile. The `id` is
read-only; `email`, `first_name`, and `last_name` can be updated. `PUT` replaces
the editable fields; `PATCH` updates only supplied fields.

Example `PATCH` request:

```json
{
  "first_name": "Sam"
}
```

Response:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "staff@example.com",
  "first_name": "Sam",
  "last_name": "Taylor"
}
```

## Properties

### List or create properties

`GET, POST /properties`

`GET` returns all properties, each including its nested `units` array.

`POST` request:

```json
{
  "name": "Central Apartments",
  "address": "1 Main Street"
}
```

Response fields: `id`, `name`, `address`, `units`, and `created_at`. New
properties have an empty `units` array. IDs and timestamps are read-only.

### Retrieve or edit a property

`GET, PUT, PATCH /properties/{property_id}`

The response has the same fields as a property in the list response, including
its nested units.

`PUT` requires `name` and `address`; `PATCH` accepts either field. The nested
`units` array is read-only here: property updates do not create or edit units.
Use the unit endpoints below for unit changes.

## Units

### Create a unit for a property

`POST /properties/{property_id}/units`

Request:

```json
{
  "unit_number": "U-01",
  "monthly_rent": "12000.00"
}
```

Response fields: `id`, `property`, `unit_number`, `monthly_rent`, and `status`.
The property ID is assigned from the URL. New units start with status
`"available"`. Rent must be non-negative, and unit numbers must be unique
within a property.

### List units

`GET /units`

Returns all units. Optionally filter by occupancy status:

```http
GET /units?status=available
GET /units?status=occupied
```

`status` accepts only lowercase `available` or `occupied`. Any other value
returns `400 Bad Request`.

### Retrieve or edit a unit

`GET, PUT, PATCH /units/{unit_id}`

`PUT` requires `unit_number` and `monthly_rent`; `PATCH` accepts either field.
The `property` and `status` fields are read-only. Unit status is managed by the
contract workflow, not by directly editing a unit.

## Members

### List or create members

`GET, POST /members`

`GET` returns all members.

`POST` request:

```json
{
  "full_name": "Alex Morgan",
  "email": "alex@example.com"
}
```

Response fields: `id`, `full_name`, `email`, and `created_at`. IDs and
timestamps are read-only; email addresses must be unique.

## Contracts

### List or create contracts

`GET, POST /contracts`

`GET` returns all contracts. Optional `active` filtering:

```http
GET /contracts?active=true
GET /contracts?active=false
```

`active=true` returns contracts active today; `active=false` returns contracts
not active today. A contract is active when today's date is inclusively
between its start and end dates. Values other than `true` or `false` return
`400 Bad Request`.

`POST` request:

```json
{
  "unit": "550e8400-e29b-41d4-a716-446655440002",
  "member": "550e8400-e29b-41d4-a716-446655440003",
  "start_date": "2026-10-15",
  "end_date": "2027-10-14",
  "monthly_rent": "12000.00"
}
```

`monthly_rent` is optional; if omitted, it is copied from the unit. The end
date must be on or after the start date. A unit cannot have overlapping
inclusive contract date ranges. An overlap returns `400 Bad Request`.

Response fields: `id`, `unit`, `member`, `start_date`, `end_date`,
`monthly_rent`, `total_value`, and `created_at`. `id`, `total_value`, and
`created_at` are read-only. Total value is rent multiplied by the number of
monthly billing periods; a partial period counts as a full period, and dates
on monthly anniversaries count as one period.
Contract creation synchronizes unit status based on whether a contract for the
unit is active on the creation date.
