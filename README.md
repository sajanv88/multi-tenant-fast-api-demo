# Multi-Tenant FastAPI Todo App with Beanie & MongoDB

A simple, production-style FastAPI application demonstrating multi-tenancy using [Beanie ODM](https://beanie-odm.dev/) and MongoDB. Each tenant’s data is isolated in its own database, and the app provides basic user and todo management APIs.

## Features

- **Multi-Tenancy:** Isolates data per tenant using the `X-Tenant-ID` header.
- **FastAPI:** Modern, async Python web framework.
- **Beanie ODM:** Async MongoDB models with Pydantic.
- **Todo & User APIs:** CRUD endpoints for todos and users.
- **MongoDB:** Each tenant gets a separate database.
- **uv:** Project/dependency management ([uv](https://github.com/astral-sh/uv)).

## Project Structure

```
app/
  api/         # FastAPI endpoints
  core/        # Database & tenant middleware
  models/      # Beanie ODM models
  config.py    # App configuration
```

## Quickstart

1. **Install dependencies:**
   ```bash
   uv pip install .
   ```

2. **Set up MongoDB:**
   - Ensure MongoDB is running (default: `mongodb://localhost:27017`).
   - You can override the URI in `.env`.

3. **Run the app:**
   ```bash
   uv run fastapi dev app
   ```

4. **Try the API:**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Multi-Tenancy Usage

- Pass a tenant ID in the `X-Tenant-ID` header with each request.
- Example:
  ```
  X-Tenant-ID: 1234567890abcdef12345678
  ```

## Example Endpoints

- `GET /api/todos/` — List todos (for current tenant)
- `POST /api/todos/` — Create todo
- `PUT /api/todos/{todo_id}` — Update todo
- `DELETE /api/todos/{todo_id}` — Delete todo

- `GET /api/users/` — List users
- `POST /api/users/` — Create user
- `GET /api/users/{user_id}` - Read user

## Models

- **Tenant:** Represents a tenant (organization/account).
- **User:** Belongs to a tenant.
- **Todo:** Belongs to a tenant.

## Environment Variables

- `MONGO_URI` (default: `mongodb://localhost:27017`)

## License

MIT
