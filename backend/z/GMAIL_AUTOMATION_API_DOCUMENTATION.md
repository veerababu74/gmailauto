# Gmail Handler Automation API Documentation

## Overview
This document provides comprehensive documentation for the Gmail Handler Automation API endpoints. The API provides complete CRUD operations for managing Gmail automation settings and processing data.

## Base URL
```
http://localhost:8000/api/v1/gmail-automation
```

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### 1. Random URLs Management

#### GET /random-urls
Get all random URLs with pagination and filtering.

**Query Parameters:**
- `skip` (int, default: 0): Number of items to skip
- `limit` (int, default: 100, max: 1000): Number of items to return
- `is_active` (bool, optional): Filter by active status
- `category` (str, optional): Filter by category
- `search` (str, optional): Search in URL and description

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "url": "https://example.com",
      "description": "Example website",
      "category": "news",
      "is_active": true,
      "created_at": "2025-07-13T10:00:00Z",
      "updated_at": "2025-07-13T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 100,
  "total_pages": 1
}
```

#### GET /random-urls/active
Get all active random URLs.

**Query Parameters:**
- `category` (str, optional): Filter by category

**Response:**
```json
[
  {
    "id": 1,
    "url": "https://example.com",
    "description": "Example website",
    "category": "news",
    "is_active": true,
    "created_at": "2025-07-13T10:00:00Z",
    "updated_at": "2025-07-13T10:00:00Z"
  }
]
```

#### POST /random-urls
Create a new random URL.

**Request Body:**
```json
{
  "url": "https://example.com",
  "description": "Example website",
  "category": "news",
  "is_active": true
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://example.com",
  "description": "Example website",
  "category": "news",
  "is_active": true,
  "created_at": "2025-07-13T10:00:00Z",
  "updated_at": "2025-07-13T10:00:00Z"
}
```

#### PUT /random-urls/{url_id}
Update a random URL.

**Request Body:**
```json
{
  "url": "https://updated-example.com",
  "description": "Updated description",
  "category": "updated-category",
  "is_active": false
}
```

#### DELETE /random-urls/{url_id}
Delete a random URL.

**Response:**
```json
{
  "message": "Random URL deleted successfully"
}
```

### 2. Default Senders Management

#### GET /default-senders
Get all default senders with pagination and filtering.

**Query Parameters:**
- `skip` (int, default: 0): Number of items to skip
- `limit` (int, default: 100, max: 1000): Number of items to return
- `is_active` (bool, optional): Filter by active status
- `search` (str, optional): Search in email and description

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "email": "sender@example.com",
      "description": "Main sender email",
      "is_active": true,
      "created_at": "2025-07-13T10:00:00Z",
      "updated_at": "2025-07-13T10:00:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "per_page": 100,
  "total_pages": 1
}
```

#### GET /default-senders/active
Get all active default senders.

**Response:**
```json
[
  {
    "id": 1,
    "email": "sender@example.com",
    "description": "Main sender email",
    "is_active": true,
    "created_at": "2025-07-13T10:00:00Z",
    "updated_at": "2025-07-13T10:00:00Z"
  }
]
```

#### POST /default-senders
Create a new default sender.

**Request Body:**
```json
{
  "email": "sender@example.com",
  "description": "Main sender email",
  "is_active": true
}
```

#### PUT /default-senders/{sender_id}
Update a default sender.

**Request Body:**
```json
{
  "email": "updated-sender@example.com",
  "description": "Updated description",
  "is_active": false
}
```

#### DELETE /default-senders/{sender_id}
Delete a default sender.

**Response:**
```json
{
  "message": "Default sender deleted successfully"
}
```

### 3. Connectivity Settings Management

#### GET /connectivity-settings
Get all connectivity settings with pagination and filtering.

**Query Parameters:**
- `skip` (int): Number of items to skip
- `limit` (int): Number of items to return
- `is_active` (bool, optional): Filter by active status
- `search` (str, optional): Search in setting name and description

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "setting_name": "proxy_server",
      "setting_value": "proxy.example.com:8080",
      "description": "Main proxy server configuration",
      "is_active": true,
      "created_at": "2025-07-13T10:00:00Z",
      "updated_at": "2025-07-13T10:00:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "per_page": 100,
  "total_pages": 1
}
```

#### POST /connectivity-settings
Create a new connectivity setting.

**Request Body:**
```json
{
  "setting_name": "proxy_server",
  "setting_value": "proxy.example.com:8080",
  "description": "Main proxy server configuration",
  "is_active": true
}
```

### 4. Random Website Settings Management

#### GET /random-website-settings
Get all random website settings with pagination and filtering.

#### POST /random-website-settings
Create a new random website setting.

**Request Body:**
```json
{
  "setting_name": "visit_duration_min",
  "setting_value": "30",
  "description": "Minimum time to spend on random websites (seconds)",
  "is_active": true
}
```

### 5. Spam Handler Data Processing

#### POST /spam-handler-data
Create new spam handler data entry.

**Request Body:**
```json
{
  "agent_name": "Agent_001",
  "profile_name": "profile_gmail_1",
  "sender_email": "user@gmail.com",
  "spam_emails_found": 15,
  "moved_to_inbox": 12,
  "total_time_seconds": 45.5,
  "error_occurred": false,
  "error_details": null,
  "spam_email_subjects": [
    "You've won a million dollars!",
    "Urgent: Your account will be closed"
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "agent_name": "Agent_001",
  "profile_name": "profile_gmail_1",
  "sender_email": "user@gmail.com",
  "spam_emails_found": 15,
  "moved_to_inbox": 12,
  "total_time_seconds": 45.5,
  "error_occurred": false,
  "error_details": null,
  "spam_email_subjects": [
    "You've won a million dollars!",
    "Urgent: Your account will be closed"
  ],
  "timestamp": "2025-07-13T10:00:00Z",
  "created_at": "2025-07-13T10:00:00Z",
  "updated_at": "2025-07-13T10:00:00Z"
}
```

#### GET /spam-handler-data
Get spam handler data with pagination and filtering.

**Query Parameters:**
- `skip` (int): Number of items to skip
- `limit` (int): Number of items to return
- `agent_name` (str, optional): Filter by agent name
- `profile_name` (str, optional): Filter by profile name
- `sender_email` (str, optional): Filter by sender email
- `error_occurred` (bool, optional): Filter by error status
- `date_from` (datetime, optional): Filter from date (ISO format)
- `date_to` (datetime, optional): Filter to date (ISO format)

#### GET /spam-handler-data/{data_id}
Get specific spam handler data by ID.

#### DELETE /spam-handler-data/{data_id}
Delete spam handler data entry.

### 6. Email Processing Data Handling

#### POST /email-processing-data
Create new email processing data entry.

**Request Body:**
```json
{
  "agent_name": "Agent_001",
  "profile_name": "profile_gmail_1",
  "sender_email": "user@gmail.com",
  "email_subject": "Welcome to our newsletter!",
  "is_opened": true,
  "is_link_clicked": true,
  "is_unsubscribe_clicked": false,
  "is_reply_sent": false,
  "random_website_visited": "https://example.com",
  "random_website_duration_seconds": 120.5,
  "total_duration_seconds": 180.7,
  "error_occurred": false,
  "error_details": null
}
```

**Response:**
```json
{
  "id": 1,
  "agent_name": "Agent_001",
  "profile_name": "profile_gmail_1",
  "sender_email": "user@gmail.com",
  "email_subject": "Welcome to our newsletter!",
  "is_opened": true,
  "is_link_clicked": true,
  "is_unsubscribe_clicked": false,
  "is_reply_sent": false,
  "random_website_visited": "https://example.com",
  "random_website_duration_seconds": 120.5,
  "total_duration_seconds": 180.7,
  "error_occurred": false,
  "error_details": null,
  "timestamp": "2025-07-13T10:00:00Z",
  "created_at": "2025-07-13T10:00:00Z",
  "updated_at": "2025-07-13T10:00:00Z"
}
```

#### GET /email-processing-data
Get email processing data with pagination and filtering.

**Query Parameters:**
- `skip` (int): Number of items to skip
- `limit` (int): Number of items to return
- `agent_name` (str, optional): Filter by agent name
- `profile_name` (str, optional): Filter by profile name
- `sender_email` (str, optional): Filter by sender email
- `is_opened` (bool, optional): Filter by opened status
- `is_link_clicked` (bool, optional): Filter by link clicked status
- `error_occurred` (bool, optional): Filter by error status
- `date_from` (datetime, optional): Filter from date (ISO format)
- `date_to` (datetime, optional): Filter to date (ISO format)

### 7. Bulk Operations

#### POST /random-urls/bulk-delete
Bulk delete random URLs.

**Request Body:**
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
  "deleted_count": 4,
  "failed_ids": [5]
}
```

#### POST /default-senders/bulk-delete
Bulk delete default senders.

**Request Body:**
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

### 8. Analytics and Statistics

#### GET /analytics/spam-handler-stats
Get spam handler analytics and statistics.

**Query Parameters:**
- `date_from` (datetime, optional): Filter from date (ISO format)
- `date_to` (datetime, optional): Filter to date (ISO format)
- `agent_name` (str, optional): Filter by agent name

**Response:**
```json
{
  "total_operations": 150,
  "total_spam_found": 1250,
  "total_moved_to_inbox": 1100,
  "average_time_per_operation": 42.5,
  "error_rate": 0.02,
  "top_agents": [
    {"agent_name": "Agent_001", "operations": 50},
    {"agent_name": "Agent_002", "operations": 45}
  ]
}
```

#### GET /analytics/email-processing-stats
Get email processing analytics and statistics.

**Query Parameters:**
- `date_from` (datetime, optional): Filter from date (ISO format)
- `date_to` (datetime, optional): Filter to date (ISO format)
- `agent_name` (str, optional): Filter by agent name

**Response:**
```json
{
  "total_emails_processed": 500,
  "total_opened": 450,
  "total_links_clicked": 320,
  "total_unsubscribe_clicked": 25,
  "total_replies_sent": 180,
  "open_rate": 0.9,
  "click_rate": 0.64,
  "reply_rate": 0.36,
  "average_processing_time": 75.2,
  "error_rate": 0.01
}
```

### 9. Health Check

#### GET /health
Health check endpoint for Gmail automation APIs.

**Response:**
```json
{
  "status": "healthy",
  "service": "Gmail Handler Automation API",
  "timestamp": "2025-07-13T10:30:00Z"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- 100 requests per minute per user for GET requests
- 50 requests per minute per user for POST/PUT/DELETE requests

## Data Validation

All request bodies are validated using Pydantic models. The following validation rules apply:

### Email Fields
- Must be valid email format
- Maximum 255 characters

### URL Fields
- Must be valid HTTP/HTTPS URL format
- Maximum 2048 characters

### Text Fields
- String fields have appropriate length limits
- Required fields cannot be null or empty

### Numeric Fields
- Integer fields must be non-negative
- Float fields support decimal precision

## Pagination

List endpoints support pagination with the following parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 100, max: 1000)

Response includes pagination metadata:
- `total`: Total number of items
- `page`: Current page number
- `per_page`: Items per page
- `total_pages`: Total number of pages

## Search and Filtering

Many endpoints support search and filtering:
- Search parameters perform case-insensitive partial matching
- Filter parameters support exact matching
- Date filters support ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

## Best Practices

1. **Authentication**: Always include valid JWT token in requests
2. **Error Handling**: Implement proper error handling for all response codes
3. **Pagination**: Use pagination for large result sets
4. **Rate Limiting**: Respect rate limits to avoid throttling
5. **Data Validation**: Validate data before sending requests
6. **Idempotency**: POST requests are not idempotent, use PUT for updates
7. **Timestamps**: All timestamps are in UTC ISO format
