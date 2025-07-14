# Gmail Automation Dashboard - Backend

A FastAPI backend for the Gmail automation dashboard application.

## Features

- **Authentication**: JWT-based authentication with user registration/login
- **User Management**: User profiles and settings
- **Client Management**: CRUD operations for managing email contacts/clients
- **Campaign Management**: Email campaign creation, scheduling, and tracking
- **Gmail Integration**: Ready for Gmail API integration (OAuth setup required)
- **RESTful API**: Clean API design with proper HTTP status codes
- **Database**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL/MySQL)
- **Security**: Password hashing, JWT tokens, proper access controls
- **Documentation**: Auto-generated API docs with FastAPI/OpenAPI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Uvicorn**: ASGI server for running the application
- **Passlib**: Password hashing library
- **Python-Jose**: JWT handling for Python

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and update it:

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
- Update `SECRET_KEY` for production
- Configure Gmail API credentials (optional for basic functionality)
- Set database URL if not using SQLite

### 3. Initialize Database

```bash
python startup.py
```

This will create all necessary database tables.

### 4. Create Demo Users (Optional)

```bash
python scripts/create_demo_users.py
```

This creates demo users that match the frontend demo credentials:
- admin@gmail.com / admin123
- user@gmail.com / user123
- demo@gmail.com / demo123

### 5. Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/login/json` - JSON login endpoint
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/test-token` - Test authentication token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID (admin only)
- `GET /api/v1/users/` - List all users (admin only)
- `POST /api/v1/users/gmail/connect` - Connect Gmail account
- `POST /api/v1/users/gmail/disconnect` - Disconnect Gmail account

### Clients
- `GET /api/v1/clients/` - List clients (with filtering)
- `POST /api/v1/clients/` - Create new client
- `GET /api/v1/clients/stats` - Get client statistics
- `GET /api/v1/clients/{client_id}` - Get client by ID
- `PUT /api/v1/clients/{client_id}` - Update client
- `DELETE /api/v1/clients/{client_id}` - Delete client

### Campaigns
- `GET /api/v1/campaigns/` - List campaigns (with filtering)
- `POST /api/v1/campaigns/` - Create new campaign
- `GET /api/v1/campaigns/stats` - Get campaign statistics
- `GET /api/v1/campaigns/{campaign_id}` - Get campaign by ID
- `PUT /api/v1/campaigns/{campaign_id}` - Update campaign
- `DELETE /api/v1/campaigns/{campaign_id}` - Delete campaign
- `POST /api/v1/campaigns/{campaign_id}/start` - Start campaign
- `POST /api/v1/campaigns/{campaign_id}/pause` - Pause campaign

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── users.py         # User management endpoints
│   │   │   │   ├── clients.py       # Client management endpoints
│   │   │   │   └── campaigns.py     # Campaign management endpoints
│   │   │   └── api.py              # API router configuration
│   │   └── deps.py                 # Authentication dependencies
│   ├── core/
│   │   ├── config.py               # Application configuration
│   │   ├── database.py             # Database connection setup
│   │   └── security.py             # Security utilities (JWT, password hashing)
│   ├── crud/
│   │   ├── base.py                 # Base CRUD operations
│   │   ├── crud_user.py            # User CRUD operations
│   │   ├── crud_client.py          # Client CRUD operations
│   │   └── crud_campaign.py        # Campaign CRUD operations
│   ├── models/
│   │   ├── user.py                 # User SQLAlchemy model
│   │   ├── client.py               # Client SQLAlchemy model
│   │   └── campaign.py             # Campaign SQLAlchemy model
│   ├── schemas/
│   │   ├── user.py                 # User Pydantic schemas
│   │   ├── client.py               # Client Pydantic schemas
│   │   ├── campaign.py             # Campaign Pydantic schemas
│   │   └── token.py                # Authentication schemas
│   └── db/
│       └── init_db.py              # Database initialization
├── scripts/
│   └── create_demo_users.py        # Script to create demo users
├── main.py                         # FastAPI application entry point
├── startup.py                      # Database initialization script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables example
└── README.md                       # This file
```

## Development

### Adding New Endpoints

1. Define Pydantic schemas in `app/schemas/`
2. Create SQLAlchemy models in `app/models/`
3. Implement CRUD operations in `app/crud/`
4. Add API endpoints in `app/api/api_v1/endpoints/`
5. Register routes in `app/api/api_v1/api.py`

### Database Migrations

For production, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

### Gmail API Integration

To enable Gmail functionality:

1. Create a Google Cloud Project
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Update `.env` with your Gmail API credentials
5. Implement OAuth flow in the authentication endpoints

### Testing

Run tests with pytest:

```bash
pip install pytest pytest-asyncio
pytest
```

## Production Deployment

### Environment Variables

Set these environment variables for production:

- `SECRET_KEY`: Strong secret key for JWT signing
- `DATABASE_URL`: Production database URL
- `GMAIL_CLIENT_ID` & `GMAIL_CLIENT_SECRET`: Gmail API credentials

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Database

For production, use PostgreSQL or MySQL instead of SQLite:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost/dbname
```

## Security Notes

- Always use HTTPS in production
- Set a strong `SECRET_KEY`
- Use environment variables for sensitive data
- Implement rate limiting for production
- Regularly update dependencies
- Use proper CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
