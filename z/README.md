# Gmail Automation Backend

A robust FastAPI-based backend for Gmail automation dashboard with MySQL database support, designed for production deployment on Render.

## Features

- **FastAPI** - High-performance async web framework
- **MySQL Database** - Production-ready database with connection pooling
- **JWT Authentication** - Secure user authentication
- **Gmail API Integration** - Gmail automation capabilities
- **Production Ready** - Configured for Render deployment
- **High Concurrency** - Supports 1000+ concurrent users
- **Environment-based Configuration** - Secure environment variable management

## Quick Start

### Local Development

1. **Clone and Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run Development Server**
   ```bash
   python run_server.py --reload
   ```

### Production Deployment (Render)

1. **Environment Variables**
   Set the following in your Render dashboard:
   ```bash
   ENVIRONMENT=production
   DB_TYPE=mysql
   DB_USER=fundsill_babu
   DB_PASS=Babu@7474
   DB_HOST=45.113.224.7
   DB_PORT=3306
   DB_NAME=fundsill_gmail_automation
   SECRET_KEY=your-secure-secret-key
   FRONTEND_URL=https://your-frontend-app.netlify.app
   ```

2. **Deploy**
   ```bash
   # Build Command
   pip install -r requirements.txt
   
   # Start Command
   python run_server.py --production --workers 4
   ```

## Database Configuration

### MySQL (Production)

The backend is configured to use MySQL for production with the following credentials:

```python
DB_USER = "fundsill_babu"
DB_PASS = "Babu@7474"
DB_HOST = "45.113.224.7"
DB_PORT = "3306"
DB_NAME = "fundsill_gmail_automation"
```

### Connection Features

- **Connection Pooling**: 20 base connections + 80 overflow
- **Auto-reconnect**: Handles connection drops gracefully
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **Transaction Support**: ACID compliance

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/logout` - User logout

### Gmail Integration
- `GET /api/v1/gmail/auth` - Gmail OAuth flow
- `POST /api/v1/gmail/send` - Send email
- `GET /api/v1/gmail/emails` - Get emails

### Dashboard
- `GET /api/v1/dashboard/stats` - Dashboard statistics
- `GET /api/v1/dashboard/analytics` - Analytics data

### Health Check
- `GET /api/v1/health` - Service health status
- `GET /health` - Simple health check

## Environment Variables

### Required

```bash
# Database
DB_TYPE=mysql
DB_USER=fundsill_babu
DB_PASS=Babu@7474
DB_HOST=45.113.224.7
DB_PORT=3306
DB_NAME=fundsill_gmail_automation

# Security
SECRET_KEY=your-256-bit-secret-key

# Frontend
FRONTEND_URL=https://your-frontend-app.netlify.app
BACKEND_CORS_ORIGINS=https://your-frontend-app.netlify.app
```

### Optional

```bash
# Gmail API
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## File Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── crud/             # Database operations
│   ├── db/               # Database setup
│   ├── models/           # Database models
│   └── schemas/          # Pydantic schemas
├── data/                 # Database files
├── tests/                # Test files
├── main.py               # FastAPI application
├── database.py           # Database configuration
├── run_server.py         # Server startup
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
├── Procfile              # Render deployment
└── render.yaml           # Render configuration
```

## Testing

### Test Database Connection
```bash
python test_deployment.py
```

### Run Tests
```bash
pytest tests/
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **CORS Protection**: Configurable CORS origins
- **SQL Injection Protection**: SQLAlchemy ORM
- **Environment Variables**: Sensitive data in environment

## Performance Features

- **Connection Pooling**: Efficient database connections
- **Async Support**: FastAPI async capabilities
- **Caching**: Redis support for session management
- **Load Balancing**: Multi-worker support

## Monitoring

- **Health Checks**: `/health` and `/api/v1/health` endpoints
- **Logging**: Comprehensive application logging
- **Error Handling**: Graceful error responses
- **Metrics**: Request/response metrics

## Deployment

### Render Deployment

1. **Create Web Service** on Render
2. **Set Environment Variables** from the list above
3. **Set Build Command**: `pip install -r requirements.txt`
4. **Set Start Command**: `python run_server.py --production --workers 4`
5. **Deploy** and monitor logs

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_server.py", "--production", "--workers", "4"]
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MySQL credentials
   - Verify database server is accessible
   - Ensure database exists

2. **CORS Errors**
   - Update `BACKEND_CORS_ORIGINS` with frontend URL
   - Check if frontend uses correct backend URL

3. **Environment Variables**
   - Verify all required variables are set
   - Check for typos in variable names

## Support

For issues and questions:
- Check the deployment logs
- Review environment variables
- Test database connectivity
- Verify frontend-backend URL configuration

## License

This project is licensed under the MIT License.
