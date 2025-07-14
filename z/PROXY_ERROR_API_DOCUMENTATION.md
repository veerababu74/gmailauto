# Proxy Error Management API Documentation

## Overview

The Proxy Error Management API provides comprehensive CRUD operations for tracking and managing proxy-related errors in the Gmail automation system. This API helps monitor proxy health, troubleshoot connectivity issues, and maintain system reliability.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete proxy error records
- **Dual Endpoint Support**: Available both in main API and Gmail automation handler
- **Advanced Filtering**: Filter by agent name, proxy, profile name, or search across all fields
- **Pagination Support**: Efficient handling of large datasets
- **Analytics Support**: Get error counts and statistics
- **Automatic Timestamps**: System automatically adds created_at and updated_at timestamps

## Endpoints

### Main API Endpoints (`/api/v1/proxy-errors/`)

#### Create Proxy Error
- **POST** `/api/v1/proxy-errors/`
- **Description**: Create a new proxy error record
- **Request Body**:
```json
{
    "agent_name": "string",
    "proxy": "string", 
    "error_details": "string",
    "profile_name": "string"
}
```
- **Response**: `201 Created` with the created proxy error object

#### Get All Proxy Errors
- **GET** `/api/v1/proxy-errors/`
- **Description**: Retrieve proxy errors with filtering and pagination
- **Query Parameters**:
  - `skip` (int): Number of records to skip (default: 0)
  - `limit` (int): Number of records to return (default: 100, max: 1000)
  - `agent_name` (string): Filter by agent name
  - `proxy` (string): Filter by proxy address
  - `profile_name` (string): Filter by profile name
  - `search` (string): Search across all text fields
- **Response**: Paginated list of proxy errors

#### Get Proxy Error by ID
- **GET** `/api/v1/proxy-errors/{proxy_error_id}`
- **Description**: Get a specific proxy error by ID
- **Response**: Single proxy error object

#### Update Proxy Error
- **PUT** `/api/v1/proxy-errors/{proxy_error_id}`
- **Description**: Update a proxy error record
- **Request Body**: Partial proxy error object (any fields to update)
- **Response**: Updated proxy error object

#### Delete Proxy Error
- **DELETE** `/api/v1/proxy-errors/{proxy_error_id}`
- **Description**: Delete a proxy error record
- **Response**: Deleted proxy error object

#### Get Proxy Errors by Agent
- **GET** `/api/v1/proxy-errors/agent/{agent_name}`
- **Description**: Get recent proxy errors for a specific agent
- **Query Parameters**:
  - `limit` (int): Number of recent errors to return (default: 10, max: 100)
- **Response**: List of recent proxy errors

#### Get Proxy Error Count
- **GET** `/api/v1/proxy-errors/proxy/{proxy_address}/count`
- **Description**: Get total error count for a specific proxy
- **Response**: 
```json
{
    "proxy": "proxy_address",
    "error_count": 25
}
```

#### Get Statistics
- **GET** `/api/v1/proxy-errors/stats`
- **Description**: Get proxy error statistics
- **Response**:
```json
{
    "total_errors": 150,
    "unique_agents": ["agent1", "agent2"],
    "unique_proxies": ["proxy1", "proxy2"],
    "unique_profiles": ["profile1", "profile2"]
}
```

### Gmail Automation Handler Endpoints (`/api/v1/gmail-automation/proxy-errors`)

The Gmail automation handler provides the same CRUD operations with identical functionality:

- **POST** `/api/v1/gmail-automation/proxy-errors`
- **GET** `/api/v1/gmail-automation/proxy-errors`
- **GET** `/api/v1/gmail-automation/proxy-errors/{proxy_error_id}`
- **PUT** `/api/v1/gmail-automation/proxy-errors/{proxy_error_id}`
- **DELETE** `/api/v1/gmail-automation/proxy-errors/{proxy_error_id}`
- **GET** `/api/v1/gmail-automation/proxy-errors/agent/{agent_name}`
- **GET** `/api/v1/gmail-automation/proxy-errors/proxy/{proxy_address}/count`

## Data Models

### ProxyError Model
```json
{
    "id": 1,
    "agent_name": "agent_001",
    "proxy": "192.168.1.100:8080",
    "error_details": "Connection timeout after 30 seconds",
    "profile_name": "gmail_profile_001",
    "created_at": "2025-07-13T10:30:00Z",
    "updated_at": "2025-07-13T10:30:00Z"
}
```

### Field Descriptions

- **id**: Unique identifier (auto-generated)
- **agent_name**: Name of the agent experiencing the proxy issue
- **proxy**: Proxy server address and port (e.g., "192.168.1.100:8080")
- **error_details**: Detailed description of the error
- **profile_name**: Name of the profile associated with the error
- **created_at**: Timestamp when the record was created (auto-generated)
- **updated_at**: Timestamp when the record was last updated (auto-generated)

## Database Schema

```sql
CREATE TABLE proxy_errors (
    id INTEGER PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,
    proxy VARCHAR(255) NOT NULL,
    error_details TEXT NOT NULL,
    profile_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_proxy_errors_agent_name ON proxy_errors(agent_name);
CREATE INDEX idx_proxy_errors_proxy ON proxy_errors(proxy);
CREATE INDEX idx_proxy_errors_profile_name ON proxy_errors(profile_name);
```

## Usage Examples

### Create a New Proxy Error
```bash
curl -X POST "http://localhost:8000/api/v1/proxy-errors/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "agent_name": "agent_001",
    "proxy": "192.168.1.100:8080",
    "error_details": "Connection timeout after 30 seconds",
    "profile_name": "gmail_profile_001"
  }'
```

### Get Recent Errors for an Agent
```bash
curl -X GET "http://localhost:8000/api/v1/proxy-errors/agent/agent_001?limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search for Specific Error Types
```bash
curl -X GET "http://localhost:8000/api/v1/proxy-errors/?search=timeout&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Error Count for a Proxy
```bash
curl -X GET "http://localhost:8000/api/v1/proxy-errors/proxy/192.168.1.100:8080/count" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Error Handling

The API follows standard HTTP status codes:

- **200 OK**: Successful GET requests
- **201 Created**: Successful POST requests
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server errors

Example error response:
```json
{
    "detail": "Proxy error not found"
}
```

## Authentication

All endpoints require authentication. Include the Bearer token in the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Rate Limiting

Standard rate limiting applies to all endpoints. Monitor the response headers for rate limit information.

## Integration Guidelines

### For Proxy Error Logging
1. When a proxy fails, immediately create a proxy error record
2. Include detailed error information in the `error_details` field
3. Use consistent naming for agents and profiles

### For Monitoring
1. Regularly check recent errors for active agents
2. Monitor error counts for specific proxies
3. Use the search functionality to identify patterns

### For Maintenance
1. Periodically clean up old error records
2. Archive or delete resolved issues
3. Use analytics to identify problematic proxies

## Best Practices

1. **Consistent Naming**: Use consistent naming conventions for agents and profiles
2. **Detailed Errors**: Provide detailed error descriptions for troubleshooting
3. **Regular Cleanup**: Implement regular cleanup of old error records
4. **Monitoring**: Set up monitoring for high error rates
5. **Analytics**: Use the statistics endpoints for trend analysis

## Support

For issues or questions regarding the Proxy Error Management API, please refer to the main API documentation or contact the development team.
