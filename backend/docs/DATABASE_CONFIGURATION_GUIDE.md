# Database Configuration Guide

## Overview
The Gmail Automation backend now supports both SQLite and MySQL databases with advanced connection pooling and keep-alive mechanisms designed to handle 1000+ concurrent users.

## Features
- **Dual Database Support**: SQLite for development, MySQL for production
- **Connection Pooling**: Optimized pool settings for high concurrency
- **Keep-Alive Mechanism**: Prevents connection timeouts (30-minute intervals)
- **Health Monitoring**: Built-in health checks and monitoring endpoints
- **Async Support**: Full async/await support for better performance
- **Auto-Recovery**: Automatic connection recovery and retry mechanisms

## Database Types

### SQLite (Development/Testing)
- **Pros**: Zero setup, file-based, great for development
- **Cons**: Limited concurrent write performance
- **Use Case**: Development, testing, small deployments

### MySQL (Production)
- **Pros**: High performance, excellent concurrency, scalable
- **Cons**: Requires server setup and maintenance
- **Use Case**: Production environments with 100+ concurrent users

## Configuration

### Environment Variables

```bash
# Database Type Selection
DB_TYPE=sqlite  # or 'mysql'

# SQLite Configuration
SQLITE_DATABASE_PATH=./data/gmail_dashboard.db

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=gmail_automation

# Pool Configuration (for 1000+ users)
DB_POOL_SIZE=25           # Base connections
DB_MAX_OVERFLOW=100       # Additional connections
DB_POOL_TIMEOUT=30        # Connection wait timeout
DB_POOL_RECYCLE=3600      # Recycle after 1 hour
DB_KEEP_ALIVE_INTERVAL=1800  # Keep-alive every 30 min
```

### Production MySQL Setup

1. **Create MySQL Database**:
```sql
CREATE DATABASE gmail_automation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gmail_automation_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON gmail_automation.* TO 'gmail_automation_user'@'%';
FLUSH PRIVILEGES;
```

2. **MySQL Configuration** (my.cnf):
```ini
[mysqld]
max_connections = 500
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
query_cache_size = 64M
```

3. **Use Production Environment File**:
```bash
cp .env.production.mysql .env
# Edit .env with your actual values
```

## Connection Pool Settings

### For 1000+ Concurrent Users
- **Base Pool Size**: 25 connections
- **Max Overflow**: 100 additional connections
- **Total Capacity**: 125 concurrent connections
- **Keep-Alive**: Every 30 minutes
- **Connection Recycling**: Every hour

### Pool Sizing Formula
```
Base Pool = CPU Cores × 2
Max Overflow = Expected Peak Concurrent Users ÷ 10
Total = Base Pool + Max Overflow
```

## Database Setup

### Automatic Setup
```bash
python setup_database.py
```

### Manual Setup
```python
from app.db.init_db import init_db
init_db()
```

### Async Setup
```python
from app.db.init_db import init_db_async
await init_db_async()
```

## Health Monitoring

### Health Check Endpoints
- `GET /api/v1/database/health` - Overall database health
- `GET /api/v1/database/pool-status` - Connection pool status  
- `POST /api/v1/database/test-connection` - Manual connection test

### Health Check Response
```json
{
  "status": "healthy",
  "database_type": "mysql",
  "connection_test": true,
  "pool_status": {
    "pool_size": 25,
    "checked_in": 20,
    "checked_out": 5,
    "overflow": 10,
    "invalidated": 0
  },
  "timestamp": 1704067200.0
}
```

## Performance Optimization

### MySQL Optimization
1. **Enable Query Caching**:
```sql
SET GLOBAL query_cache_type = ON;
SET GLOBAL query_cache_size = 67108864;  -- 64MB
```

2. **Optimize InnoDB**:
```sql
SET GLOBAL innodb_buffer_pool_size = 1073741824;  -- 1GB
SET GLOBAL innodb_log_file_size = 268435456;      -- 256MB
```

3. **Connection Optimization**:
```sql
SET GLOBAL max_connections = 500;
SET GLOBAL wait_timeout = 28800;
SET GLOBAL interactive_timeout = 28800;
```

### Application Optimization
- Use async endpoints for heavy operations
- Implement connection pooling properly
- Monitor pool usage regularly
- Use database transactions efficiently

## Troubleshooting

### Common Issues

1. **Connection Pool Exhausted**:
   - Increase `DB_MAX_OVERFLOW`
   - Check for connection leaks
   - Monitor slow queries

2. **MySQL Connection Timeouts**:
   - Verify `DB_KEEP_ALIVE_INTERVAL`
   - Check MySQL `wait_timeout` setting
   - Ensure firewall allows persistent connections

3. **SQLite Lock Errors**:
   - Switch to MySQL for high concurrency
   - Reduce concurrent write operations
   - Use WAL mode for SQLite

### Debug Mode
```bash
DB_ECHO=true  # Enable SQL query logging
```

### Monitoring Commands
```python
from app.core.database import db_manager

# Check connection status
print(db_manager.test_connection())

# Get pool status
print(db_manager.get_pool_status())

# Health check
from app.core.database import check_database_health
print(check_database_health())
```

## Migration from Old System

### Update Imports
```python
# Old
from app.core.database import get_db, engine, SessionLocal

# New (same imports work, enhanced backend)
from app.core.database import get_db, engine, SessionLocal
```

### Environment Migration
1. Copy existing `.env` file
2. Add new database configuration variables
3. Set `DB_TYPE=sqlite` for existing SQLite setups
4. Run `python setup_database.py` to verify

## Security Considerations

1. **MySQL Security**:
   - Use strong passwords
   - Enable SSL connections
   - Limit user privileges
   - Regular security updates

2. **Connection Security**:
   - Use connection encryption
   - Implement connection limits
   - Monitor for suspicious activity

3. **Environment Variables**:
   - Never commit `.env` files
   - Use secrets management in production
   - Rotate database passwords regularly

## Production Deployment

### Docker Configuration
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: gmail_automation
      MYSQL_USER: gmail_automation_user
      MYSQL_PASSWORD: user_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: >
      mysqld
      --max_connections=500
      --innodb_buffer_pool_size=1G
      
  backend:
    build: .
    environment:
      DB_TYPE: mysql
      MYSQL_HOST: mysql
      MYSQL_USER: gmail_automation_user
      MYSQL_PASSWORD: user_password
    depends_on:
      - mysql

volumes:
  mysql_data:
```

### Kubernetes Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gmail-automation-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gmail-automation-backend
  template:
    metadata:
      labels:
        app: gmail-automation-backend
    spec:
      containers:
      - name: backend
        image: gmail-automation-backend:latest
        env:
        - name: DB_TYPE
          value: "mysql"
        - name: DB_POOL_SIZE
          value: "25"
        - name: DB_MAX_OVERFLOW
          value: "100"
        # Add other environment variables
```

## Performance Benchmarks

### Expected Performance
- **SQLite**: ~100 concurrent users
- **MySQL (Basic)**: ~500 concurrent users  
- **MySQL (Optimized)**: ~1000+ concurrent users

### Load Testing
```bash
# Install artillery for load testing
npm install -g artillery

# Test database endpoints
artillery run database-load-test.yml
```

This configuration is designed to handle enterprise-level traffic while maintaining optimal performance and reliability.
