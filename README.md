# Multi-User Project & Issue Management API

A production-style REST API built with FastAPI for managing users, projects, project memberships, issues, and comments.

The project demonstrates backend architecture, authentication, authorization, relational database design, validation, pagination, filtering, testing, logging, and Docker-based deployment.

---

## 🚀 Features

- **User registration and authentication** with JWT tokens and Argon2 password hashing.
- **Role-based access control (RBAC)** supporting `ADMIN`, `MANAGER`, and `MEMBER` roles.
- **Project & Membership Management** to safely control which users can access specific project resources.
- **Issue Tracking** with dedicated assignments, status lifecycles, and priority management.
- **Interactive Commenting System** attached directly to project issues.
- **Robust API Design** featuring Pydantic request/response validation, robust error handling, and built-in pagination/filtering.
- **Reliable Infrastructure** backed by a MySQL database using SQLAlchemy ORM, fully containerized via Docker Compose with data persistence.

---

## 🏗️ Architecture

The application follows a layered backend architecture:

```text
Client ──> Router ──> Service ──> Repository ──> Database
```

### Layer Breakdown

* **Router**: Handles HTTP requests, endpoint routing, parameters, authentication dependencies, and responses.
* **Service**: Contains the core business logic, application rules, and resource authorization policies.
* **Repository**: Directs database interaction and abstracts CRUD operations using the SQLAlchemy ORM.
* **Models**: Defines database schemas, structures, table constraints, and relational mappings.
* **Schemas**: Manages strict request validation payloads and response serialization via Pydantic.
* **Security**: Handles password hashing operations, JWT issuance, and authentication checks.

---

## 🛠️ Tech Stack

* **Core Framework**: Python, FastAPI, Uvicorn
* **Data Validation**: Pydantic
* **Database & ORM**: MySQL, SQLAlchemy, PyMySQL
* **Security & Auth**: PyJWT, pwdlib (Argon2 backend)
* **Testing**: Pytest
* **DevOps & Infrastructure**: Docker, Docker Compose

---

## 📁 Project Structure

```text
project-management-api/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── project_member.py
│   │   ├── issue.py
│   │   └── comment.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── project.py
│   │   ├── issue.py
│   │   └── comment.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   ├── issues.py
│   │   └── comments.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   └── issue_service.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── issue_repository.py
│   │   └── comment_repository.py
│   │
│   ├── security/
│   │   ├── password.py
│   │   ├── jwt.py
│   │   └── auth.py
│   │
│   └── logging_config.py
│
├── tests/
│   └── test_main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Authentication & Authorization

### Authentication
The API utilizes stateless **JWT-based authentication**. Users register and log in to receive an access token required for protected endpoints.

#### Registration (`POST /auth/register`)
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Login (`POST /auth/login`)
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Authorization (RBAC)
* **ADMIN**: Grants full administrative access to all application resources.
* **MANAGER**: Allows creation and structural management of assigned projects, memberships, and issues.
* **MEMBER**: Grants read/write access to project contexts they explicitly belong to.

---

## 📌 Main API Endpoints

### Authentication
* `POST /auth/register` - Create a new user account
* `POST /auth/login` - Authenticate and receive a access token

### Users
* `GET /users/me` - Retrieve current user profile
* `GET /users/admin-test` - Restricted endpoint for checking admin access

### Projects
* `POST /projects` - Create a new project
* `GET /projects` - List all projects (supports pagination: `?page=1&limit=20`)
* `POST /projects/{project_id}/members/{user_id}` - Add user to project
* `GET /projects/{project_id}/members` - View project member roster
* `DELETE /projects/{project_id}/members/{user_id}` - Remove member from project

### Issues
* `POST /projects/{project_id}/issues` - Create a new project issue
* `GET /projects/{project_id}/issues` - List project issues with filters (e.g., `?status=OPEN&priority=HIGH&page=1&limit=10`)
* `GET /issues/{issue_id}` - Retrieve issue details
* `PUT /issues/{issue_id}` - Update issue status, priority, or details
* `DELETE /issues/{issue_id}` - Remove an issue
* `POST /issues/{issue_id}/assign/{user_id}` - Assign an issue to a user

### Comments
* `POST /issues/{issue_id}/comments` - Leave a comment on an issue
* `GET /issues/{issue_id}/comments` - Fetch comment history for an issue
* `PUT /comments/{comment_id}` - Modify an existing comment
* `DELETE /comments/{comment_id}` - Delete a comment

#### Filter Criteria Matrix
* **Supported Statuses**: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`
* **Supported Priorities**: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

---

## 🗄️ Database Design

The system runs on **MySQL** utilizing explicit relational mappings. The `project_members` association table acts as the join entity for many-to-many configurations.

```text
User 1 ──────── * Project
User * ──────── * Project (via project_members)
Project 1 ───── * Issue
User 1 ──────── * Issue
Issue 1 ─────── * Comment
User 1 ──────── * Comment
```

---

## ⚙️ Configuration

To set up the environment configuration, duplicate the template file and fill in your secrets:

```bash
cp .env.example .env
```

Ensure your `.env` contains the required keys:
```env
DATABASE_URL=mysql+pymysql://root:your_password@db:3306/project_management_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
*Note: Do not commit your final `.env` file to version control.*

---

## 🐳 Docker Deployment

The application runs seamlessly inside microservices orchestrated by **Docker Compose**.

### Network & Data Architecture
```text
                  Docker Compose
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       FastAPI API           MySQL DB
        Container            Container
             │                   │
             └──── Docker ───────┘
                   Network
                       │
                 mysql_data
                    Volume
```

### Steps to Run
1. Start up the entire environment:
   ```bash
   docker compose up --build
   ```
2. Open your browser and view the application:
   * **Base API Endpoint**: `http://localhost:8000`
   * **Interactive Swagger UI Docs**: `http://localhost:8000/docs`

### Managing Data Persistence
Database changes persist on your host machine inside the `mysql_data` Docker volume.
* **Stop services cleanly**: `docker compose down`
* **Hard reset (Wipe database)**: `docker compose down -v` *(Warning: This permanently deletes your stored database records).*

---

## 🧪 Testing

The system evaluates endpoint behavior using targeted unit tests with Pytest and the FastAPI TestClient. Database actions are isolated using FastAPI dependency overrides.

Run the test suite locally with:
```bash
pytest
```

---

## 📊 Error Handling & Logging

### Error States
The application catches exceptions centrally and responds with consistent structure using semantic HTTP status codes:
* `400 Bad Request` — General invalid payloads
* `401 Unauthorized` — Invalid or missing JWT tokens
* `403 Forbidden` — Insufficient authorization roles or member mismatch
* `404 Not Found` — Resource missing
* `409 Conflict` — Data duplication (e.g., email already registered)
* `422 Validation Error` — Pydantic schema rule breach
* `500 Internal Server Error` — Uncaught backend failure

### Logging Management
Python's native `logging` library is configured to emit application logs directly to stdout, eliminating unsafe print statements. Sensitive elements like passwords or signature keys are automatically filtered and omitted.

Stream your live container logs with:
```bash
docker compose logs -f api
```

---