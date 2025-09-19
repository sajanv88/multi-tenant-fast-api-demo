# Multi-Tenant FastAPI Todo App with Beanie & MongoDB

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![Beanie](https://img.shields.io/badge/Beanie-ODM-orange.svg)](https://beanie-odm.dev/)

A **demonstration project** showcasing the basics of **multi-tenancy** architecture using [Beanie ODM](https://beanie-odm.dev/) and MongoDB. This educational example implements **database-per-tenant** isolation to show how tenant data can be separated in different MongoDB databases.

## 🚀 Key Features

- **🏢 Multi-Tenancy Demo**: Basic data isolation with separate databases per tenant
- **⚡ FastAPI**: Modern, high-performance async Python web framework  
- **🍃 Beanie ODM**: Elegant async MongoDB ODM built on Pydantic
- **📋 Simple CRUD**: Basic operations for todos and users
- **🔒 Tenant Middleware**: Simple tenant detection via headers
- **📊 MongoDB**: NoSQL database with async operations
- **🛠️ uv**: Lightning-fast Python package manager
- **📚 Educational**: Great starting point for learning multi-tenancy concepts Multi-Tenant FastAPI Todo App with Beanie & MongoDB 

A simple, production-style FastAPI application demonstrating multi-tenancy using [Beanie ODM](https://beanie-odm.dev/) and MongoDB. Each tenant’s data is isolated in its own database, and the app provides basic user and todo management APIs.

## Features

- **Multi-Tenancy:** Isolates data per tenant using the `X-Tenant-ID` header.
- **FastAPI:** Modern, async Python web framework.
- **Beanie ODM:** Async MongoDB models with Pydantic.
- **Todo & User APIs:** CRUD endpoints for todos and users.
- **MongoDB:** Each tenant gets a separate database.
- **uv:** Project/dependency management ([uv](https://github.com/astral-sh/uv)).

## 🏗️ Basic Multi-Tenancy Architecture

This demo application shows a simple **database-per-tenant** pattern:

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Client    │───▶│   FastAPI App    │───▶│   MongoDB Cluster   │
│             │    │                  │    │                     │
│ X-Tenant-ID │    │ Tenant Middleware│    │ ┌─────────────────┐ │
│   Header    │    │                  │    │ │ tenant_123_db   │ │
└─────────────┘    │ Dynamic Database │    │ ├─────────────────┤ │
                   │    Selection     │    │ │ tenant_456_db   │ │
                   └──────────────────┘    │ ├─────────────────┤ │
                                           │ │ tenant_789_db   │ │
                                           │ └─────────────────┘ │
                                           └─────────────────────┘
```

### How the Demo Works

1. **Tenant Identification**: Each request includes an `X-Tenant-ID` header (no validation in this demo)
2. **Middleware Processing**: Simple middleware extracts the tenant ID
3. **Database Selection**: Beanie connects to tenant-specific database (`tenant_{id}_db`)
4. **Basic Data Isolation**: Operations are scoped to the tenant's database
5. **Auto-Creation**: New tenant databases are created automatically

> **⚠️ Note**: This is a basic demonstration. Production apps need authentication, validation, error handling, and security measures.

## 📁 Project Structure

```
multi-tenant-fast-api-demo/
├── app/
│   ├── __init__.py
│   ├── config.py              # Application configuration
│   ├── api/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── tenant_endpoint.py # Tenant management APIs
│   │   ├── todo_endpoint.py   # Todo CRUD operations
│   │   └── user_endpoint.py   # User management APIs
│   ├── core/                  # Core application logic
│   │   ├── __init__.py
│   │   ├── database.py        # MongoDB connection & Beanie setup
│   │   └── tenant_middleware.py # Multi-tenant middleware
│   └── models/                # Beanie ODM models
│       ├── __init__.py
│       ├── app_base.py        # Base model with tenant isolation
│       ├── tenant.py          # Tenant model
│       ├── todo.py            # Todo model
│       └── user.py            # User model
├── pyproject.toml             # Project dependencies (uv)
├── uv.lock                    # Locked dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- MongoDB (running locally or remote)
- [uv](https://github.com/astral-sh/uv) package manager

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sajanv88/multi-tenant-fast-api-demo.git
   cd multi-tenant-fast-api-demo
   ```

2. **Install dependencies using uv:**
   ```bash
   uv pip install .
   ```

3. **Set up MongoDB:**
   - **Local MongoDB**: Ensure MongoDB is running on `mongodb://localhost:27017`
   - **Remote MongoDB**: Set the `MONGO_URI` environment variable
   ```bash
   export MONGO_URI="mongodb://your-mongodb-uri"
   ```

4. **Run the application:**
   ```bash
   uv run fastapi dev app
   ```

5. **Access the API:**
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🏢 Multi-Tenancy Demo

### Understanding the Basic Isolation

Every API request **should** include the `X-Tenant-ID` header. This demo uses this ID to determine which database to use for data storage and retrieval.

> **⚠️ Demo Limitation**: This example doesn't validate tenant IDs or implement authentication and host access permissions - any string can be used as a tenant ID.

```bash
# Example: Creating a tenant as a host
curl -X POST "http://localhost:8000/api/tenants/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corporation" }'
```

### Simple Demo Walkthrough

#### 1. Create Two Different Demo Tenants

**Tenant 1: Company ABC**
```bash
curl -X POST "http://localhost:8000/api/tenants/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Company ABC" }'
```

**Tenant 2: Company XYZ**
```bash
curl -X POST "http://localhost:8000/api/tenants/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Company XYZ" }'
```

#### 2. Create Users for Each Tenant

**User for Company ABC:**
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: company-abc-123" \
  -d '{"name": "Alice Smith", "email": "alice@companyabc.com"}'
```

**User for Company XYZ:**
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: company-xyz-456" \
  -d '{"name": "Bob Johnson", "email": "bob@companyxyz.com"}'
```

#### 3. Create Todos for Each Tenant

**Todo for Company ABC:**
```bash
curl -X POST "http://localhost:8000/api/todos/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: company-abc-123" \
  -d '{"title": "Implement new feature", "description": "Add user authentication", "completed": false}'
```

**Todo for Company XYZ:**
```bash
curl -X POST "http://localhost:8000/api/todos/" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: company-xyz-456" \
  -d '{"title": "Review code", "description": "Review pull request #123", "completed": false}'
```

#### 4. Verify Data Isolation

**List todos for Company ABC (should only see ABC's todos):**
```bash
curl -X GET "http://localhost:8000/api/todos/" \
  -H "X-Tenant-ID: company-abc-123"
```

**List todos for Company XYZ (should only see XYZ's todos):**
```bash
curl -X GET "http://localhost:8000/api/todos/" \
  -H "X-Tenant-ID: company-xyz-456"
```

> **🔒 Basic Data Isolation**: Each tenant will only see their own data, demonstrating the core concept of multi-tenancy!

## 📚 Basic Endpoint Overview

### Tenant Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tenants/` | List all tenants |
| `POST` | `/api/tenants/` | Create a new tenant |
| `GET` | `/api/tenants/{tenant_id}` | Get current tenant info |

### User Management  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/users/` | List all users (tenant-scoped) |
| `POST` | `/api/users/` | Create a new user |
| `GET` | `/api/users/{user_id}` | Get user by ID |

### Todo Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/todos/` | List all todos (tenant-scoped) |
| `POST` | `/api/todos/` | Create a new todo |
| `GET` | `/api/todos/{todo_id}` | Get todo by ID |
| `PUT` | `/api/todos/{todo_id}` | Update todo |
| `DELETE` | `/api/todos/{todo_id}` | Delete todo |

> **📝 Note**: All endpoints in this demo automatically scope data to the tenant specified in the `X-Tenant-ID` header (no validation performed) excepts Tenant endpoint.

## Lets understand the basic important concept
   The most important concept in Multitenancy is `Host` vs `Tenants`

   - The host is responsible for owning and overseeing the management of the SaaS application’s system.
   - A tenant refers to a paying customer of the SaaS application who utilizes the service.


## 🗄️ Simple Database Models

### Basic Model Structure

This demo uses simple **Beanie ODM** models to show tenant isolation: Refer `models` folder.


## ⚙️ Basic Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |

### Example `.env` file:
```bash
MONGO_URI=mongodb://localhost:27017

```

## 🧪 Testing the Demo

You can test the basic multi-tenancy concept using:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Don't forget to add the `X-Tenant-ID` header!
- **curl**: See the examples above
- **Postman**: Create requests with different `X-Tenant-ID` headers
- **Python requests**:

```python
import requests

# Demo: Two different tenant IDs (can be any string in this demo)
headers_tenant_1 = {"X-Tenant-ID": "demo-tenant-1"}
headers_tenant_2 = {"X-Tenant-ID": "demo-tenant-2"}

# Create todo for demo tenant 1
requests.post(
    "http://localhost:8000/api/todos/",
    json={"title": "Tenant 1 Todo", "description": "Only visible to tenant 1"},
    headers=headers_tenant_1
)

# Create todo for demo tenant 2  
requests.post(
    "http://localhost:8000/api/todos/",
    json={"title": "Tenant 2 Todo", "description": "Only visible to tenant 2"},
    headers=headers_tenant_2
)

# Each tenant will only see their own todos (basic isolation demo)
todos_tenant_1 = requests.get("http://localhost:8000/api/todos/", headers=headers_tenant_1)
todos_tenant_2 = requests.get("http://localhost:8000/api/todos/", headers=headers_tenant_2)
```

## ⚠️ What This Demo Doesn't Include (Production Requirements)

This is a **basic educational demo**. For production use, you would need to add:

### 🔐 Security & Authentication
- **Tenant Authentication**: Verify that users belong to the tenant they claim
- **API Authentication**: JWT tokens, API keys, or OAuth2
- **Tenant ID Validation**: Ensure tenant IDs are valid and authorized
- **Rate Limiting**: Prevent abuse and ensure fair usage

### 🛡️ Data Protection
- **Input Validation**: Comprehensive request validation and sanitization
- **Data Encryption**: Encrypt sensitive data at rest and in transit
- **Audit Logging**: Track all tenant operations for compliance

### 🚀 Performance & Reliability
- **Connection Pooling**: Efficient database connection management
- **Caching Strategy**: Redis or similar for improved performance
- **Error Handling**: Comprehensive error handling and user-friendly responses
- **Health Checks**: Monitoring and alerting for system health

### 📊 Operations & Monitoring
- **Logging**: Structured logging with tenant context
- **Metrics**: Tenant-specific performance metrics
- **Backup & Recovery**: Tenant-aware backup strategies
- **Database Migrations**: Safe schema changes across tenant databases

### 🏗️ Architecture Improvements
- **Tenant Onboarding**: Automated tenant provisioning
- **Resource Limits**: Per-tenant resource quotas and limits
- **Load Balancing**: Distribute load across multiple instances
- **Circuit Breakers**: Fault tolerance patterns

## 📚 Learning Resources

This demo is great for learning the basics! To build production multi-tenant apps, study:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Beanie ODM Documentation](https://beanie-odm.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Multi-Tenancy](https://en.wikipedia.org/wiki/Multitenancy)

## 🤝 Contributing

This is a learning project! Feel free to:

1. Fork the repository
2. Add features or improvements (`git checkout -b feature/improvement`)
3. Add better examples or documentation
4. Submit a Pull Request with your enhancements

Ideas for contributions:
- Add authentication examples
- Implement tenant validation
- Add more comprehensive error handling
- Create Docker setup
- Add unit tests

## 📄 License

MIT License - perfect for learning and experimenting with multi-tenancy concepts!

---


**Happy learning! 🎉**
