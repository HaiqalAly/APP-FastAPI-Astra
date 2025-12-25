# FastAPI Codename: Astra - Learning Backend Development

## Project Background
> A learning project from my 3rd semester (sophomore year) where I'm teaching myself backend development beyond what's covered in class. Trying to understand how real APIs work by building one myself.

## Getting Started

### Prerequisites
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- [Docker](https://www.docker.com/) - For running PostgreSQL and the app

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Create a `.env` file in the root directory with your configuration or just use the provided .env.example (delete the .example):
   ```env
   SECRET_KEY=your-secret-key-here
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database

   POSTGRES_TEST_USER=test_user
   POSTGRES_TEST_PASSWORD=test_password
   POSTGRES_TEST_DB=test_db
   ```
4. Build and start the containers:
   ```bash
   docker compose up --build
   ```
5. The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

## What I've Built So Far

### Basic Setup (Working)
- **FastAPI App**: Got a basic async API running with FastAPI. Still learning how all the async/await stuff actually works.
- **PostgreSQL + Docker**: Database runs in Docker containers. Took a while to figure out docker-compose but it's working now.
- **Alembic Migrations**: Database versioning tool. Made 2 migrations so far - one for user activation and one for roles. Struggled a lot getting Alembic to work with async SQLAlchemy - kept running into sync/async conflicts. Eventually found a template in the Alembic docs for pyproject_async setups and used that instead. Still not 100% confident with migrations.

### Authentication (Mostly Working)
- **JWT Tokens**: Applied JWT authentication patterns with a focus on token lifecycle management.
- **Password Hashing**: Implemented industry-standard PBKDF2-SHA256 hashing via Passlib.
- **Register/Login**: Basic endpoints work. Added some validation like password requirements (8 chars, uppercase, lowercase, digit).
- **Token Refresh**: Got the refresh token endpoint working after some trial and error with the token validation.

### Authorization (Functional but Basic)
- **Role System**: Added ADMIN, MODERATOR, and USER roles. Evaluating the scalability of this RBAC implementation for future growth.
- **Protected Routes**: Dependency injection for checking roles. Seems like a FastAPI pattern but still wrapping my head around how dependencies compose.
- **Few Protected Endpoints**: Made a couple test endpoints for admin/moderator access to make sure the role checking works.

### Database (Learning as I Go)
- **SQLAlchemy 2.0**: Using the new async version. Confusing rating 10/10.
- **User Model**: Basic table with username, email, password hash, role, and timestamps. Pretty standard stuff.
- **CRUD Functions**: Can create users, look them up by username/email, and authenticate. Nothing fancy.

### What Could Be Better
- **Testing**: Only have 3 basic tests. Current priority is core feature development; expanding async test coverage is in the roadmap.
- **Error Messages**: Some error messages are vague. Should make them more user-friendly.
- **Security**: Probably missing some security best practices I don't know about yet.
- **Code Organization**: Some files are getting messy. Not sure if my separation of concerns is actually good.
- **Documentation**: No proper API docs setup besides the auto-generated FastAPI ones.
- **Logging**: Barely any logging. Just print statements in some places.

### What's Missing
- Email verification (no email service configured)
- Password reset (seems complicated with tokens and email)
- User profile updates (can create users but can't update them yet)
- Rate limiting (no idea how to implement this properly maybe Redis?)
- Proper test coverage (maybe 20% covered?)
- CI/CD (haven't learned this yet)
- Production deployment considerations (environment configs are basic)

### Tech Stack
- **uv** - Fast Python package manager (use `uv sync` to install dependencies)
- **FastAPI** - Python web framework (async)
- **PostgreSQL** - Database
- **SQLAlchemy 2.0** - ORM (async version)
- **Alembic** - Database migrations
- **Docker & Docker Compose** - Containerization
- **PyJWT** - JWT tokens
- **Passlib** - Password hashing
- **Pytest** - Testing (barely)

### Current State
The API works for basic user registration and authentication. You can create an account, login, get a token, and access protected routes. It's functional but definitely a learning project with rough edges. I'm learning a lot about async Python, database design, and API security patterns.

### What I'm Learning
- Async programming is harder than I thought
- Database sessions and connection management is tricky
- Security is more complex than "just hash the password"
- Docker is really helpful once you get past the initial learning curve
- FastAPI's dependency injection is powerful but takes time to understand
- Writing tests makes you realize how many edge cases you missed
