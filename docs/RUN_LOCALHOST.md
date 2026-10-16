# Run the API on localhost

The API uses PostgreSQL. Choose either Docker Compose (quickest) or run Django
directly with a locally installed PostgreSQL server.

The API base URL is `http://127.0.0.1:8000/api/`. See the
[API reference](./API.md) for endpoints and request examples.

## Option 1: Docker Compose

Prerequisites: Docker Engine and the Docker Compose plugin.

1. From the project root, copy the example environment file and edit `.env`:

   ```sh
   cp .envexample .env
   ```

   Set `POSTGRES_PASSWORD` and `SECRET_KEY` to local values. `.env` is excluded
   from source control.

2. Build and start the API and PostgreSQL:

   ```sh
   docker compose up --build
   ```

   Compose waits until PostgreSQL is healthy and applies database migrations
   before starting the API.

3. Open `http://127.0.0.1:8000/api/` or use the endpoints documented in the
   [API reference](./API.md). Application logs appear in the terminal.

4. Stop the services with `Ctrl+C`, then:

   ```sh
   docker compose down
   ```

   PostgreSQL data is retained in the `postgres_data` volume. To remove that
   data as well, use `docker compose down --volumes`.

## Option 2: Run Django directly

Prerequisites: Python 3.10+, PostgreSQL 13+, and `psql` command-line tools.

1. Start PostgreSQL, then create a database user and database. For a local
   PostgreSQL installation on Linux, open a PostgreSQL shell:

   ```sh
   sudo -u postgres psql
   ```

   Run these SQL statements there, substituting a local development password:

   ```sql
   CREATE USER pms_user WITH PASSWORD 'local-dev-password';
   CREATE DATABASE property_management OWNER pms_user;
   \q
   ```

   If you already have a PostgreSQL user and database, use those credentials
   in the `.env` file instead.

2. Copy the example environment file and edit `.env` in the project root:

   ```sh
   cp .envexample .env
   ```

   Set `POSTGRES_USER=pms_user`, `POSTGRES_PASSWORD` to the password created
   above, and `SECRET_KEY` to a long random local value. Keep
   `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5432`. Django loads this file
   automatically. Environment variables exported in your shell take
   precedence over values in `.env`.

3. Create and activate a virtual environment, then install dependencies:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Apply migrations, check the Django configuration, and start the development
   server:

   ```sh
   python manage.py migrate
   python manage.py check
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/api/`. Stop the server with `Ctrl+C`.

## Register and log in

In a second terminal, register a staff account:

```sh
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"staff@example.com","password":"StrongPass123","first_name":"Sam"}'
```

Log in to obtain JWT access and refresh tokens:

```sh
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"staff@example.com","password":"StrongPass123"}'
```

Use the returned access token as `Authorization: Bearer <access-token>` on
protected API requests. See the [API reference](./API.md) for all routes.

## Troubleshooting

- **`no password supplied` or password authentication failed:** ensure
  `POSTGRES_PASSWORD` is set in `.env` and matches the PostgreSQL user's
  password. Restart Django after changing environment settings.
- **Connection refused:** confirm PostgreSQL is running and that
  `POSTGRES_HOST` and `POSTGRES_PORT` point to it. For direct Django runs,
  `POSTGRES_HOST` is usually `localhost`; in Compose it is `db`.
- **Database does not exist:** create the database named by `POSTGRES_DB` and
  grant ownership or access to `POSTGRES_USER`.
- **Port 8000 is already in use:** stop the other service or run
  `python manage.py runserver 8001` for direct Django runs.
