# Logged Out Profiles API Implementation

## Overview

The Logged Out Profiles API has been successfully implemented with full CRUD operations. This API allows you to track when profiles get logged out, with automatic timestamp generation.

## Features Implemented

### 1. Database Model
- **Table**: `logged_out_profiles`
- **Fields**:
  - `id` (Primary Key, Auto-increment)
  - `agent_name` (String, Required, Indexed)
  - `profile_name` (String, Required, Indexed)
  - `timestamp` (DateTime, Auto-generated, Indexed)
  - `created_at` (DateTime, Auto-generated)
  - `updated_at` (DateTime, Auto-updated)

### 2. API Endpoints

#### Gmail Automation Handler Endpoint (As Requested)
```
POST /gmail-automation/logged-out-profiles
```

**Request Body:**
```json
{
    "agent_name": "Agent_001",
    "profile_name": "profile_gmail_1"
}
```

**Response:**
```json
{
    "id": 1,
    "agent_name": "Agent_001", 
    "profile_name": "profile_gmail_1",
    "timestamp": "2025-07-13T10:30:00Z",
    "created_at": "2025-07-13T10:30:00Z",
    "updated_at": "2025-07-13T10:30:00Z"
}
```

#### Full CRUD API Endpoints
```
POST   /api/v1/logged-out-profiles/              # Create new record
GET    /api/v1/logged-out-profiles/              # List all records (with pagination and filters)
GET    /api/v1/logged-out-profiles/{id}          # Get specific record
PUT    /api/v1/logged-out-profiles/{id}          # Update record
DELETE /api/v1/logged-out-profiles/{id}          # Delete record
POST   /api/v1/logged-out-profiles/bulk-delete   # Bulk delete multiple records
GET    /api/v1/logged-out-profiles/agent/{agent_name}  # Get records by agent
GET    /api/v1/logged-out-profiles/analytics/stats     # Get analytics
```

### 3. Query Parameters (for GET endpoints)

- `skip`: Number of records to skip (pagination)
- `limit`: Number of records to return (max 1000)
- `agent_name`: Filter by agent name
- `profile_name`: Filter by profile name
- `date_from`: Filter from date (ISO format)
- `date_to`: Filter to date (ISO format)
- `search`: Search in agent_name and profile_name

### 4. Analytics Endpoint

**GET `/api/v1/logged-out-profiles/analytics/stats`**

Returns statistics like:
```json
{
    "total_logouts": 150,
    "top_agents": [
        {"agent_name": "Agent_001", "logout_count": 50}
    ],
    "top_profiles": [
        {"profile_name": "profile_gmail_1", "logout_count": 30}
    ]
}
```

## Files Created/Modified

### New Files Created:
1. `app/models/logged_out_profile.py` - Database model
2. `app/schemas/logged_out_profile.py` - Pydantic schemas
3. `app/crud/crud_logged_out_profile.py` - CRUD operations
4. `app/api/endpoints/logged_out_profiles.py` - Full API endpoints
5. `scripts/create_logged_out_profiles_table.py` - Database migration script
6. `test_logged_out_profiles_api.py` - Test script

### Modified Files:
1. `gmailhandlerautomation.py` - Added POST endpoint and schemas
2. `app/models/__init__.py` - Added new model import
3. `app/api/api_v1/api.py` - Added router for full API

## How to Use

### 1. Database Setup
The database table has already been created. If you need to recreate it:
```bash
python scripts/create_logged_out_profiles_table.py
```

### 2. Start the Server
```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the API
```bash
python test_logged_out_profiles_api.py
```

### 4. Example Usage

#### Create a logged out profile entry:
```bash
curl -X POST "http://localhost:8000/gmail-automation/logged-out-profiles" \
     -H "Content-Type: application/json" \
     -d '{
       "agent_name": "Agent_001",
       "profile_name": "profile_gmail_1"
     }'
```

#### Get all logged out profiles:
```bash
curl "http://localhost:8000/api/v1/logged-out-profiles/"
```

#### Get profiles by agent:
```bash
curl "http://localhost:8000/api/v1/logged-out-profiles/agent/Agent_001"
```

#### Get analytics:
```bash
curl "http://localhost:8000/api/v1/logged-out-profiles/analytics/stats"
```

## Key Features

### ✅ Automatic Timestamp Generation
The `timestamp` field is automatically set to the current UTC time when a record is created.

### ✅ Full CRUD Operations
- Create, Read, Update, Delete operations
- Bulk delete functionality
- Pagination and filtering
- Search functionality

### ✅ Analytics Support
- Get statistics by agent and profile
- Date range filtering
- Top agents/profiles by logout count

### ✅ Error Handling
- Proper HTTP status codes
- Detailed error messages
- Input validation

### ✅ Documentation
- Complete API documentation with examples
- Request/response schemas
- Query parameter descriptions

## Integration with Existing Code

The implementation follows the same patterns as other APIs in your system:
- Uses the same database session management
- Follows the same CRUD pattern
- Uses the same response models
- Integrates seamlessly with the existing router structure

## Next Steps

1. **Test the implementation** using the provided test script
2. **Integrate with your frontend** using the API endpoints
3. **Add authentication** if needed (following the same pattern as other endpoints)
4. **Customize fields** if you need additional data tracked

The implementation is production-ready and follows all the best practices used in your existing codebase.
