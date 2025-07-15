# Simple Render Deployment Guide

## Files Structure
This project has been cleaned up to remove all Docker, YAML, shell scripts, and Procfile dependencies for a simple Render deployment.

## Required Files
- `requirements.txt` - Contains only essential Python dependencies
- `main.py` - Main FastAPI application entry point
- `run_server.py` - Simple server startup script for Render

## Render Deployment Steps

### 1. Connect Your Repository
- Connect your GitHub repository to Render
- Select "Web Service" as the service type

### 2. Configure Build & Deploy Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python run_server.py`
- **Environment**: `Python 3`

### 3. Environment Variables
Set these environment variables in Render dashboard:

```
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DB_TYPE=sqlite
SQLITE_DATABASE_PATH=./data/gmail_dashboard.db
FRONTEND_URL=https://your-frontend-url.com
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REDIRECT_URI=https://your-backend-url.com/api/v1/auth/gmail/callback
```

### 4. Database Setup
The application uses SQLite by default, which will work on Render's filesystem (though data will be lost on redeploys). For persistent data, you can:
- Use Render's PostgreSQL addon
- Set `DB_TYPE=mysql` and configure MySQL environment variables

### 5. Deploy
- Click "Deploy" in Render dashboard
- Monitor the deployment logs
- Your API will be available at the provided Render URL

## Local Development
To run locally:
```bash
pip install -r requirements.txt
python run_server.py
```

## API Endpoints
- Health check: `GET /health`
- API documentation: `GET /docs`
- Main API: `GET /api/v1/`

## Notes
- CORS is configured to allow all origins for simplicity
- The application will automatically create the SQLite database on first run
- All complex deployment configurations have been removed for simplicity
