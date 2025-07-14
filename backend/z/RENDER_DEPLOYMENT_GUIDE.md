# Gmail Automation Backend - Render Deployment Guide

## Prerequisites
- Render account
- MySQL database credentials (cPanel hosting)
- Gmail API credentials (optional)
- SMTP credentials (optional)

## Environment Variables Setup

### Required Environment Variables for Render:

```bash
# Project Configuration
ENVIRONMENT=production
HOST=0.0.0.0
PORT=10000

# Database Configuration
DB_TYPE=mysql
DB_USER=fundsill_babu
DB_PASS=Babu@7474
DB_HOST=45.113.224.7
DB_PORT=3306
DB_NAME=fundsill_gmail_automation

# MySQL Configuration (Alternative naming)
MYSQL_HOST=45.113.224.7
MYSQL_PORT=3306
MYSQL_USER=fundsill_babu
MYSQL_PASSWORD=Babu@7474
MYSQL_DATABASE=fundsill_gmail_automation

# Security (Generate a secure secret key)
SECRET_KEY=your-256-bit-secret-key-here

# CORS Configuration (Replace with your frontend URL)
FRONTEND_URL=https://your-frontend-app.netlify.app
BACKEND_CORS_ORIGINS=https://your-frontend-app.netlify.app,http://localhost:5173

# Gmail API (Optional - for Gmail integration)
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REDIRECT_URI=https://your-backend-app.onrender.com/api/v1/auth/gmail/callback

# SMTP Configuration (Optional - for email notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_TLS=true
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Deployment Steps

### Method 1: Using Render Dashboard

1. **Create New Web Service**
   - Go to your Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Build Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_server.py --production --workers 4`
   - **Environment**: Python 3

3. **Set Environment Variables**
   - Copy all environment variables from the list above
   - Set them in the Render dashboard under "Environment"

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Method 2: Using render.yaml (Infrastructure as Code)

1. **Update render.yaml**
   - Edit the `render.yaml` file in the backend directory
   - Update the `FRONTEND_URL` and `BACKEND_CORS_ORIGINS` with your actual URLs

2. **Deploy**
   - Push the `render.yaml` file to your repository
   - In Render dashboard, create a new service using the YAML file

## Database Migration

After deployment, you may need to run database migrations:

1. **Access Render Shell**
   - Go to your service dashboard
   - Click "Shell" tab
   - Run migration commands if needed

2. **Test Database Connection**
   - Your application will automatically create tables on first run
   - Check logs for any database connection issues

## Health Check

The application includes a health check endpoint at `/api/v1/health` that Render will use to monitor your service.

## Monitoring

1. **Logs**: Monitor application logs in the Render dashboard
2. **Metrics**: Check CPU, memory, and response times
3. **Health**: Monitor the health check endpoint status

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**
   - Verify MySQL credentials
   - Check if database server allows external connections
   - Ensure database name exists

2. **CORS Issues**
   - Update `BACKEND_CORS_ORIGINS` with your frontend URL
   - Check if frontend is making requests to correct backend URL

3. **Environment Variables**
   - Ensure all required environment variables are set
   - Check for typos in variable names

4. **Build Failures**
   - Check requirements.txt for package conflicts
   - Verify Python version compatibility

## Security Considerations

1. **Secret Key**: Generate a secure 256-bit secret key
2. **Database**: Use strong database passwords
3. **CORS**: Only allow necessary origins
4. **HTTPS**: Ensure all URLs use HTTPS in production

## Frontend Integration

Update your frontend to use the Render backend URL:

```javascript
// Replace localhost with your Render URL
const API_BASE_URL = 'https://your-backend-app.onrender.com/api/v1';
```

## Support

For issues related to:
- Database connectivity: Check MySQL server status
- API endpoints: Review FastAPI documentation
- Deployment: Check Render logs and documentation
