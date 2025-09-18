# NeuroNotes

A full-stack knowledge management system with graph visualization capabilities. NeuroNotes allows users to create, organize, and visualize topics and notes in an interconnected knowledge graph with tagging and relationship management.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Vite + Tailwind CSS v4.0+
- **Database**: PostgreSQL with pgvector extension
- **Architecture**: Monolithic structure optimized for deployment on Render

## Features

- **User Authentication**: Secure JWT-based authentication and authorization
- **Topic Management**: Create and organize topics with graph positioning
- **Note Management**: Rich note creation with URL attachments and tagging
- **Tag System**: Flexible tagging system for note categorization
- **Graph Visualization**: Topics can be positioned for graph-based visualization
- **RESTful API**: Clean, well-documented REST API endpoints
- **Database Integration**: PostgreSQL with pgvector support for future vector operations

## Project Structure

```
NeuroNotes/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/routes/     # HTTP interface layer
│   │   ├── core/              # Infrastructure and configuration
│   │   ├── data/repository/   # Data access layer
│   │   ├── domain/            # Business logic layer
│   │   ├── dtos/              # Data transfer objects
│   │   └── models/            # Database models (SQLModel)
│   ├── alembic/               # Database migrations
│   ├── main.py               # Backend entry point
│   └── requirements.txt      # Python dependencies
├── frontend/             # React frontend application
│   ├── src/                  # Source code
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Vite configuration
└── README.md            # Project documentation
```

## Architecture

### Backend - Clean Architecture Implementation

The FastAPI backend follows Clean Architecture principles with clear separation of concerns:

**Key Architectural Components:**

- **Domain Layer**: Business logic and use cases isolated from external dependencies
- **Repository Pattern**: Clean data access abstraction
- **Result Pattern**: Functional error handling with `Success[T]` and `Error[E]` types
- **Dependency Injection**: FastAPI's built-in DI for repository and service management

### Frontend - React + Vite + Tailwind CSS

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS v4.0+ for utility-first styling
- **Development**: Hot reload and modern development experience

### Backend Technology Stack

- **Framework**: FastAPI 0.116.1+
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLModel (SQLAlchemy + Pydantic integration)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic models with comprehensive validation rules
- **Migrations**: Alembic for database schema management

## Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL 12+** (database)
- **pgvector extension** (for future vector operations)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Tanmoy-Sarkar-Pranto/NeuroNotes-FastAPI.git
cd NeuroNotes-FastAPI
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
# Or alternatively: pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb neuronotes

# Install pgvector extension (optional, for future use)
psql -d neuronotes -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 5. Environment Configuration
Create a `.env` file in the `backend` directory:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/neuronotes
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/neuronotes

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### 6. Database Migration
```bash
cd backend

# Run migrations to create tables
alembic upgrade head
```

### 7. Start the Application

#### Quick Start (Recommended)
```bash
# Start both servers simultaneously
./start-dev.sh      # On macOS/Linux
start-dev.bat       # On Windows
```

This will start:
- **Backend API**: `http://localhost:8000`
- **Frontend App**: `http://localhost:5173`
- **API Documentation**: `http://localhost:8000/docs`

#### Individual Server Startup

##### Backend (API)
```bash
cd backend

# Development server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

##### Frontend (React App)
```bash
cd frontend

# Development server
npm run dev
```

## API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoint Documentation
Detailed API documentation is available in separate markdown files:

- [`auth.md`](./auth.md) - Authentication endpoints (register, login)
- [`user.md`](./user.md) - User profile management
- [`topic.md`](./topic.md) - Topic CRUD operations
- [`note.md`](./note.md) - Note management with tag support
- [`tag.md`](./tag.md) - Tag system for note organization

### API Overview

**Base URL**: `http://localhost:8000/api/v1`

**Core Endpoints**:
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /user/` - Get current user profile
- `CRUD /topics/` - Topic management
- `CRUD /notes/` - Note management with tagging
- `CRUD /tags/` - Tag management

**Authentication**: All protected endpoints require JWT Bearer token:
```
Authorization: Bearer <access_token>
```

## Usage Examples

### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com", 
    "password": "SecurePass123!"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Create a Topic
```bash
curl -X POST "http://localhost:8000/api/v1/topics/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning",
    "description": "Notes about ML concepts",
    "position": {"x": 100, "y": 200}
  }'
```

### 4. Create a Note with Tags
```bash
curl -X POST "http://localhost:8000/api/v1/notes/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Neural Networks",
    "content": "Deep learning fundamentals...",
    "topic_id": "<topic_uuid>",
    "tag_ids": ["<tag_uuid_1>", "<tag_uuid_2>"]
  }'
```

## Database Schema

### Core Entities

**Users**
- Authentication and user management
- Relationships to topics, notes, and tags

**Topics** 
- Knowledge organization units
- Graph positioning for visualization
- Unique titles per user

**Notes**
- Content storage with optional titles
- URL attachments support
- Many-to-many relationship with tags

**Tags**
- Note categorization system
- User-scoped with optional colors
- Reusable across multiple notes

### Relationships
- Users → Topics (1:N)
- Users → Notes (1:N) 
- Users → Tags (1:N)
- Topics → Notes (1:N)
- Notes ↔ Tags (N:M)

## Development

### Project Structure
```
NeuroNotes-FastAPI/
├── app/
│   ├── api/v1/routes/      # API route handlers
│   ├── core/               # Configuration and dependencies
│   ├── data/repository/    # Data access layer
│   ├── domain/             # Business logic
│   ├── dtos/              # API response models
│   ├── models/            # Database models
│   └── util/              # Utility functions
├── alembic/               # Database migrations
├── main.py               # Application entry point
└── requirements.txt      # Dependencies
```

### Adding New Features

1. **Define Models**: Add SQLModel definitions in `app/models/`
2. **Create Repository**: Implement data access in `app/data/repository/`
3. **Business Logic**: Add use cases in `app/domain/use_case/`
4. **API Routes**: Create endpoints in `app/api/v1/routes/`
5. **Documentation**: Update relevant `.md` files

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Testing
```bash
# Run the application
python main.py

# Test endpoints with curl or HTTP client
# Use interactive docs at http://localhost:8000/docs
```

## Security Features

- **Password Security**: bcrypt hashing with salt
- **JWT Authentication**: Stateless token-based auth
- **Input Validation**: Comprehensive Pydantic validation
- **CORS Configuration**: Configurable cross-origin support
- **User Isolation**: All resources scoped to authenticated users

## Deployment

### Environment Variables
Set these environment variables in production:
- `SECRET_KEY`: Strong secret key for JWT signing
- `DATABASE_URL`: Production database connection
- `ENVIRONMENT`: Set to "production"
- `BACKEND_CORS_ORIGINS`: Allowed origins for CORS

### Production Considerations
- Use environment-specific configuration
- Set up proper database connection pooling
- Configure logging and monitoring
- Set up SSL/TLS termination
- Use a production WSGI server (e.g., gunicorn)

---

For detailed API usage and examples, refer to the individual endpoint documentation files in this repository.