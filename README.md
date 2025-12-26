# FastAPI Authentication API - Codename: Astra

> **Student Learning Project** - A self-directed exploration of backend development fundamentals during my sophomore year. This project represents my journey in understanding modern web API architecture, authentication patterns, and asynchronous Python programming.

## Overview

A RESTful API built with FastAPI implementing JWT-based authentication and role-based access control (RBAC). This project serves as both a practical learning experience and a portfolio piece demonstrating foundational backend development skills.

### Project Goals
- Understand asynchronous programming patterns in Python
- Implement secure authentication and authorization mechanisms
- Practice database design and ORM usage
- Learn containerization with Docker
- Apply software engineering best practices in a real-world context

## Features

### ✅ Implemented
- **User Authentication**
  - Registration with input validation
  - Login with JWT access and refresh tokens
  - Token refresh mechanism
  - Password hashing using PBKDF2-SHA256 via Passlib

- **Authorization**
  - Role-based access control (ADMIN, MODERATOR, USER)
  - Protected endpoints using FastAPI dependency injection
  - Permission validation middleware

- **Database**
  - PostgreSQL with async SQLAlchemy 2.0
  - User model with timestamps and role management
  - Alembic migrations for schema versioning

- **Infrastructure**
  - Docker Compose orchestration
  - Separate development and test databases
  - Health checks and service dependencies

### 🚧 Areas for Improvement
- Test coverage (currently minimal, focused on core auth flows)
- Comprehensive logging and monitoring
- Enhanced error messages and validation feedback
- Email verification system
- Password reset functionality
- User profile management endpoints
- Rate limiting implementation

## Tech Stack
- Framework: FastAPI (async)
- Database: PostgreSQL 16
- ORM: SQLAlchemy 2.0 (async)
- Migrations: Alembic
- Authentication: PyJWT (Access & Refresh Tokens)
- Security: Passlib (PBKDF2-SHA256)
- Testing: Pytest + Pytest-Asyncio
- Containerization: Docker & Docker Compose
- Package Manager: uv
- Code Style: Ruff

## Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- [Docker Desktop](https://www.docker.com/) - For containerized services

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HaiqalAly/APP-FastAPI-Astra
   cd APP-FastAPI-Astra
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root (or rename `.env.example`):
   ```env
   SECRET_KEY=your-secret-key-here
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database

   POSTGRES_TEST_USER=test_user
   POSTGRES_TEST_PASSWORD=test_password
   POSTGRES_TEST_DB=test_db
   ```

4. **Start the application**
   ```bash
   docker compose up --build
   ```

5. **Access the API**
   - API: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Development Scripts

Helper scripts are available in the `scripts/` directory:
- `run.sh` - Start the application
- `down.sh` - Stop services
- `logs.sh` - View container logs
- `watch.sh` - Development mode with hot reload

## API Structure

```
app/
├── api/v1/endpoints/    # API route handlers
│   ├── auth.py         # Authentication endpoints
│   ├── users.py        # User management
│   ├── admin.py        # Admin operations
│   └── moderator.py    # Moderator operations
├── core/               # Core functionality
│   ├── config.py       # Configuration management
│   ├── security.py     # Security utilities
│   └── exceptions.py   # Custom exceptions
├── db/                 # Database layer
│   ├── connection.py   # Database connection
│   ├── crud.py         # Database operations
│   └── models/         # SQLAlchemy models
├── schemas/            # Pydantic schemas
└── services/           # Business logic
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Key Learning Outcomes

Through this project, I've gained practical experience with:

- **Asynchronous Programming**: Understanding async/await patterns, event loops, and managing async database sessions
- **Authentication & Security**: Implementing JWT tokens, password hashing, and secure credential management
- **Database Management**: Schema design, migrations, and the complexities of async ORM operations
- **API Design**: RESTful principles, endpoint structuring, and response modeling
- **Dependency Injection**: Leveraging FastAPI's DI system for clean, testable code
- **Containerization**: Docker orchestration, service dependencies, and development workflows
- **Testing**: Writing async tests and understanding the importance of comprehensive test coverage

## Project Status

**Current State**: Functional MVP with core authentication features operational

This project is under active development as a learning exercise. While the implemented features are functional and follow industry patterns, there are known areas for enhancement and refinement. Feedback and suggestions for improvement are welcome.

## Acknowledgments

This project was built by following best practices from official documentation, community resources, and online tutorials. Special thanks to the FastAPI, SQLAlchemy, and Python communities for their excellent documentation and support materials.

## License

See [LICENSE](LICENSE) file for details.

---

*Built with curiosity and determination by a student learning backend development one endpoint at a time.*
