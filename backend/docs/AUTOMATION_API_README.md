# Gmail Automation Backend - Settings API

This document describes the comprehensive CRUD API system for managing Gmail automation settings.

## Overview

The backend provides four main categories of automation settings:

1. **Default Senders** - Email addresses for default senders
2. **Random URLs** - Websites for random browsing during automation
3. **Random Website Settings** - Configuration for random website feature
4. **Connectivity Settings** - Configuration for connectivity management

## API Structure

All APIs follow RESTful conventions and provide comprehensive CRUD operations:

- `GET` - Retrieve data (with pagination, filtering, and search)
- `POST` - Create new records
- `PUT` - Update existing records
- `DELETE` - Delete records
- Bulk operations for efficiency
- Configuration endpoints for automation integration

## Base URL

All API endpoints are prefixed with: `/api/v1/`

## Authentication

Currently, the APIs don't require authentication, but they can be easily secured by adding the `get_current_user` dependency to any endpoint.

## API Endpoints

### 1. Default Senders API (`/api/v1/default-senders`)

Manages email addresses used as default senders in the automation.

#### Endpoints:

- `GET /` - List all default senders with pagination
- `GET /active` - Get all active default senders
- `GET /emails` - Get list of email addresses only
- `GET /{sender_id}` - Get single default sender by ID
- `POST /` - Create new default sender
- `POST /bulk` - Bulk create default senders
- `PUT /{sender_id}` - Update default sender
- `DELETE /{sender_id}` - Delete single default sender
- `DELETE /bulk/delete` - Bulk delete default senders
- `DELETE /` - Delete all default senders
- `PUT /activate/all` - Activate all default senders
- `PUT /deactivate/all` - Deactivate all default senders

#### Example Usage:

```bash
# Get all active default senders
curl -X GET "http://localhost:8000/api/v1/default-senders/active"

# Create a new default sender
curl -X POST "http://localhost:8000/api/v1/default-senders/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "description": "Test sender",
    "is_active": true
  }'

# Get email addresses only (for automation)
curl -X GET "http://localhost:8000/api/v1/default-senders/emails"
```

### 2. Random URLs API (`/api/v1/random-urls`)

Manages websites used for random browsing during automation.

#### Endpoints:

- `GET /` - List all random URLs with pagination and filtering
- `GET /active` - Get all active random URLs
- `GET /urls` - Get list of URLs only
- `GET /categories` - Get all unique categories
- `GET /by-category/{category}` - Get URLs by category
- `GET /random` - Get random shuffled URLs
- `GET /{url_id}` - Get single random URL by ID
- `POST /` - Create new random URL
- `POST /bulk` - Bulk create random URLs
- `PUT /{url_id}` - Update random URL
- `DELETE /{url_id}` - Delete single random URL
- `DELETE /bulk/delete` - Bulk delete random URLs
- `DELETE /` - Delete all random URLs
- `PUT /activate/all` - Activate all random URLs
- `PUT /deactivate/all` - Deactivate all random URLs

#### Example Usage:

```bash
# Get random URLs for automation
curl -X GET "http://localhost:8000/api/v1/random-urls/random?limit=5"

# Create a new random URL
curl -X POST "http://localhost:8000/api/v1/random-urls/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.example.com",
    "description": "Example website",
    "category": "other",
    "is_active": true
  }'

# Get URLs by category
curl -X GET "http://localhost:8000/api/v1/random-urls/by-category/social"
```

### 3. Random Website Settings API (`/api/v1/random-website-settings`)

Manages configuration settings for the random website browsing feature.

#### Endpoints:

- `GET /` - List all settings with pagination
- `GET /active` - Get all active settings
- `GET /config` - Get configuration as dictionary
- `GET /config/structured` - Get structured configuration object
- `GET /by-name/{setting_name}` - Get setting by name
- `GET /{setting_id}` - Get setting by ID
- `POST /` - Create new setting
- `POST /initialize-defaults` - Initialize default settings
- `PUT /{setting_id}` - Update setting by ID
- `PUT /by-name/{setting_name}` - Update setting by name
- `PUT /bulk/update` - Bulk update settings
- `PUT /config/update` - Update complete configuration
- `DELETE /{setting_id}` - Delete setting
- `POST /reset-to-defaults` - Reset to default values

#### Available Settings:

- `ENABLE_RANDOM_WEBSITES` (boolean) - Enable/disable random website feature
- `RANDOM_WEBSITE_MIN_DURATION` (integer) - Minimum browsing duration
- `RANDOM_WEBSITE_MAX_DURATION` (integer) - Maximum browsing duration
- `RANDOM_SITE_MIN_DURATION` (integer) - Minimum site visit duration
- `RANDOM_SITE_MAX_DURATION` (integer) - Maximum site visit duration
- `EMAIL_TAB_CLOSE_DURATION` (integer) - Email tab close duration
- `DEFAULT_TIMEOUT` (integer) - Default operation timeout
- `LINK_CLICK_WAIT` (integer) - Wait time after clicking links

#### Example Usage:

```bash
# Get configuration for automation
curl -X GET "http://localhost:8000/api/v1/random-website-settings/config"

# Update a specific setting
curl -X PUT "http://localhost:8000/api/v1/random-website-settings/by-name/ENABLE_RANDOM_WEBSITES?setting_value=true"

# Bulk update settings
curl -X PUT "http://localhost:8000/api/v1/random-website-settings/bulk/update" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "ENABLE_RANDOM_WEBSITES": true,
      "RANDOM_WEBSITE_MIN_DURATION": 20,
      "RANDOM_WEBSITE_MAX_DURATION": 45
    }
  }'
```

### 4. Connectivity Settings API (`/api/v1/connectivity-settings`)

Manages configuration settings for connectivity management.

#### Endpoints:

- `GET /` - List all settings with pagination
- `GET /active` - Get all active settings
- `GET /config` - Get configuration as dictionary
- `GET /config/structured` - Get structured configuration object
- `GET /test-urls` - Get connectivity test URLs
- `GET /by-name/{setting_name}` - Get setting by name
- `GET /{setting_id}` - Get setting by ID
- `POST /` - Create new setting
- `POST /initialize-defaults` - Initialize default settings
- `POST /test-urls` - Add new test URL
- `PUT /{setting_id}` - Update setting by ID
- `PUT /by-name/{setting_name}` - Update setting by name
- `PUT /bulk/update` - Bulk update settings
- `PUT /config/update` - Update complete configuration
- `PUT /test-urls/update` - Update all test URLs
- `DELETE /{setting_id}` - Delete setting
- `DELETE /test-urls/{url}` - Remove test URL
- `POST /reset-to-defaults` - Reset to default values

#### Available Settings:

- `ENABLE_CONNECTIVITY_MANAGER` (boolean) - Enable/disable connectivity management
- `CONNECTIVITY_CHECK_TIMEOUT` (integer) - Timeout for connectivity checks
- `CONNECTIVITY_MAX_RETRIES` (integer) - Maximum retry attempts
- `CONNECTIVITY_RETRY_DELAY` (integer) - Delay between retries
- `CONNECTIVITY_CHECK_INTERVAL` (integer) - Interval between checks
- `CONNECTIVITY_MAX_WAIT_TIME` (integer) - Maximum wait time
- `CONNECTIVITY_TEST_URLS` (array) - URLs for connectivity testing

#### Example Usage:

```bash
# Get connectivity configuration
curl -X GET "http://localhost:8000/api/v1/connectivity-settings/config"

# Get test URLs
curl -X GET "http://localhost:8000/api/v1/connectivity-settings/test-urls"

# Add a new test URL
curl -X POST "http://localhost:8000/api/v1/connectivity-settings/test-urls" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/status/200"}'
```

### 5. Unified Automation API (`/api/v1/automation`)

Provides unified access to all automation configurations.

#### Endpoints:

- `GET /automation-config` - Get complete automation configuration
- `GET /automation-config/default-senders` - Get default senders only
- `GET /automation-config/random-urls` - Get random URLs only
- `GET /automation-config/random-website` - Get random website settings only
- `GET /automation-config/connectivity` - Get connectivity settings only
- `POST /automation-config/initialize` - Initialize all default settings
- `GET /health` - Health check

#### Example Usage:

```bash
# Get complete automation configuration (for your automation system)
curl -X GET "http://localhost:8000/api/v1/automation/automation-config"

# Initialize all default settings
curl -X POST "http://localhost:8000/api/v1/automation/automation-config/initialize"
```

## Database Models

### Default Sender
```python
{
  "id": int,
  "email": str,
  "description": str,
  "is_active": bool,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Random URL
```python
{
  "id": int,
  "url": str,
  "description": str,
  "category": str,
  "is_active": bool,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Settings (Random Website & Connectivity)
```python
{
  "id": int,
  "setting_name": str,
  "setting_value": str,
  "setting_type": str,  # 'boolean', 'integer', 'float', 'string', 'array'
  "description": str,
  "is_active": bool,
  "created_at": datetime,
  "updated_at": datetime
}
```

## Setup and Installation

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Initialize database and default settings:**
   ```bash
   python setup_automation.py
   ```

3. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API documentation:**
   Open http://localhost:8000/docs in your browser

## Integration with Existing Automation Code

To integrate with your existing automation code, update your API client to use these new endpoints:

```python
# Example integration
import requests

class AutomationAPIClient:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def get_settings(self):
        """Get all automation settings"""
        response = requests.get(f"{self.base_url}/automation/automation-config")
        return response.json()
    
    def get_default_senders(self):
        """Get default senders"""
        response = requests.get(f"{self.base_url}/automation/automation-config/default-senders")
        return response.json()["DEFAULT_SENDERS"]
    
    def get_random_urls(self):
        """Get random URLs"""
        response = requests.get(f"{self.base_url}/automation/automation-config/random-urls")
        return response.json()["RANDOM_URLS"]
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `500` - Internal Server Error

Error responses include detailed error messages:

```json
{
  "detail": "Error description"
}
```

## Performance Features

- **Pagination**: All list endpoints support `skip` and `limit` parameters
- **Filtering**: Filter by `is_active`, `category`, `setting_type`, etc.
- **Search**: Full-text search in relevant fields
- **Bulk Operations**: Efficient bulk create/update/delete operations
- **Database Optimization**: Proper indexing on frequently queried fields

## Security Considerations

- Input validation using Pydantic schemas
- SQL injection protection through SQLAlchemy ORM
- Email validation for sender addresses
- URL validation for random URLs
- Setting type validation for configuration values

## Future Enhancements

1. **Authentication & Authorization**: Add user-based access control
2. **Audit Logging**: Track changes to settings with timestamps and user info
3. **Configuration Versioning**: Version control for settings changes
4. **Real-time Updates**: WebSocket support for real-time configuration updates
5. **Export/Import**: Backup and restore functionality for settings
6. **Scheduled Updates**: Automatic configuration updates based on schedules
