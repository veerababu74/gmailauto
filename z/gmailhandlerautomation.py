"""
Gmail Handler Automation API
Comprehensive API endpoints for Gmail automation handling including:
- Random URLs management
- Default senders management
- Connectivity settings management
- Random website settings management
- Spam handler data processing
- Email processing data handling
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, HttpUrl, validator
from datetime import datetime
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_default_sender import default_sender
from app.crud.crud_random_url import random_url
from app.crud.crud_connectivity_settings import connectivity_settings
from app.crud.crud_random_website_settings import random_website_settings
from app.crud.crud_spam_handler_data import spam_handler_data
from app.crud.crud_email_processing_data import email_processing_data
from app.crud.crud_proxy_error import proxy_error
from app.crud.crud_logged_out_profile import logged_out_profile
from app.schemas.user import User

# Initialize router
router = APIRouter(prefix="/gmail-automation", tags=["Gmail Automation Handler"])

# ================================
# PYDANTIC SCHEMAS
# ================================


# Random URLs Schemas
class RandomUrlBase(BaseModel):
    url: HttpUrl
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True


class RandomUrlCreate(RandomUrlBase):
    pass


class RandomUrlUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class RandomUrlResponse(RandomUrlBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RandomUrlListResponse(BaseModel):
    items: List[RandomUrlResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Default Senders Schemas
class DefaultSenderBase(BaseModel):
    email: EmailStr
    description: Optional[str] = None
    is_active: bool = True


class DefaultSenderCreate(DefaultSenderBase):
    pass


class DefaultSenderUpdate(BaseModel):
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DefaultSenderResponse(DefaultSenderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DefaultSenderListResponse(BaseModel):
    items: List[DefaultSenderResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Connectivity Settings Schemas
class ConnectivitySettingsBase(BaseModel):
    setting_name: str
    setting_value: str
    description: Optional[str] = None
    is_active: bool = True


class ConnectivitySettingsCreate(ConnectivitySettingsBase):
    pass


class ConnectivitySettingsUpdate(BaseModel):
    setting_name: Optional[str] = None
    setting_value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ConnectivitySettingsResponse(ConnectivitySettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConnectivitySettingsListResponse(BaseModel):
    items: List[ConnectivitySettingsResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Random Website Settings Schemas
class RandomWebsiteSettingsBase(BaseModel):
    setting_name: str
    setting_value: str
    description: Optional[str] = None
    is_active: bool = True


class RandomWebsiteSettingsCreate(RandomWebsiteSettingsBase):
    pass


class RandomWebsiteSettingsUpdate(BaseModel):
    setting_name: Optional[str] = None
    setting_value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RandomWebsiteSettingsResponse(RandomWebsiteSettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RandomWebsiteSettingsListResponse(BaseModel):
    items: List[RandomWebsiteSettingsResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Spam Handler Data Schemas
class SpamHandlerDataCreate(BaseModel):
    agent_name: str
    profile_name: str
    sender_email: EmailStr
    spam_emails_found: int = 0
    moved_to_inbox: int = 0
    total_time_seconds: float = 0.0
    error_occurred: bool = False
    error_details: Optional[str] = None
    spam_email_subjects: Optional[List[str]] = None
    timestamp: Optional[datetime] = None


class SpamHandlerDataResponse(BaseModel):
    id: int
    agent_name: str
    profile_name: str
    sender_email: str
    spam_emails_found: int
    moved_to_inbox: int
    total_time_seconds: float
    error_occurred: bool
    error_details: Optional[str]
    spam_email_subjects: Optional[List[str]]
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpamHandlerDataListResponse(BaseModel):
    items: List[SpamHandlerDataResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Email Processing Data Schemas
class EmailProcessingDataCreate(BaseModel):
    agent_name: str
    profile_name: str
    sender_email: EmailStr
    email_subject: str
    is_opened: bool = False
    is_link_clicked: bool = False
    is_unsubscribe_clicked: bool = False
    is_reply_sent: bool = False
    random_website_visited: Optional[str] = None
    random_website_duration_seconds: Optional[float] = 0.0
    total_duration_seconds: Optional[float] = 0.0
    error_occurred: bool = False
    error_details: Optional[str] = None
    timestamp: Optional[datetime] = None


class EmailProcessingDataResponse(BaseModel):
    id: int
    agent_name: str
    profile_name: str
    sender_email: str
    email_subject: str
    is_opened: bool
    is_link_clicked: bool
    is_unsubscribe_clicked: bool
    is_reply_sent: bool
    random_website_visited: Optional[str]
    random_website_duration_seconds: Optional[float]
    total_duration_seconds: Optional[float]
    error_occurred: bool
    error_details: Optional[str]
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailProcessingDataListResponse(BaseModel):
    items: List[EmailProcessingDataResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Bulk Operation Schemas
class BulkDeleteRequest(BaseModel):
    ids: List[int]


class BulkDeleteResponse(BaseModel):
    deleted_count: int
    failed_ids: List[int] = []


# Proxy Error Schemas
class ProxyErrorBase(BaseModel):
    agent_name: str
    proxy: str
    error_details: str
    profile_name: str


class ProxyErrorCreate(ProxyErrorBase):
    pass


class ProxyErrorUpdate(BaseModel):
    agent_name: Optional[str] = None
    proxy: Optional[str] = None
    error_details: Optional[str] = None
    profile_name: Optional[str] = None


class ProxyErrorResponse(ProxyErrorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProxyErrorListResponse(BaseModel):
    items: List[ProxyErrorResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# Logged Out Profile Schemas
class LoggedOutProfileBase(BaseModel):
    agent_name: str
    profile_name: str


class LoggedOutProfileCreate(LoggedOutProfileBase):
    pass


class LoggedOutProfileUpdate(BaseModel):
    agent_name: Optional[str] = None
    profile_name: Optional[str] = None


class LoggedOutProfileResponse(LoggedOutProfileBase):
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoggedOutProfileListResponse(BaseModel):
    items: List[LoggedOutProfileResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# ================================
# RANDOM URLS ENDPOINTS
# ================================


@router.get("/random-urls", response_model=List[str])
async def get_random_urls(
    db: Session = Depends(get_db),
):
    """
    Get all random URLs

    **Request:** No request body required

    **Response:**
    ```json
    [
        "https://example1.com",
        "https://example2.com",
        "https://news.site.com",
        "https://tech.blog.com"
    ]
    ```
    """
    items, _ = random_url.get_multi(
        db,
        skip=0,
        limit=None,  # No limit to get all items
        is_active=None,
        category=None,
        search=None,
    )

    # Extract just the URLs as strings
    return [str(item.url) for item in items]


# ================================
# DEFAULT SENDERS ENDPOINTS
# ================================


@router.get("/default-senders", response_model=List[str])
async def get_default_senders(
    db: Session = Depends(get_db),
):
    """
    Get all default senders

    **Request:** No request body required

    **Response:**
    ```json
    [
        "sender1@example.com",
        "sender2@company.com",
        "admin@business.org",
        "noreply@service.net"
    ]
    ```
    """
    items, _ = default_sender.get_multi(
        db, skip=0, limit=None, is_active=None, search=None
    )

    # Extract just the email addresses as strings
    return [item.email for item in items]


# ================================
# CONNECTIVITY SETTINGS ENDPOINTS
# ================================


@router.get("/connectivity-settings", response_model=List[ConnectivitySettingsResponse])
async def get_connectivity_settings(
    db: Session = Depends(get_db),
):
    """
    Get all connectivity settings

    **Request:** No request body required

    **Response:**
    ```json
    [
        {
            "id": 1,
            "setting_name": "proxy_server",
            "setting_value": "proxy.example.com:8080",
            "description": "Main proxy server configuration",
            "is_active": true,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "setting_name": "timeout_seconds",
            "setting_value": "30",
            "description": "Connection timeout in seconds",
            "is_active": true,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ]
    ```
    """
    items, _ = connectivity_settings.get_multi(
        db, skip=0, limit=None, is_active=None, search=None
    )

    return items


# ================================
# RANDOM WEBSITE SETTINGS ENDPOINTS
# ================================


@router.get(
    "/random-website-settings", response_model=List[RandomWebsiteSettingsResponse]
)
async def get_random_website_settings(
    db: Session = Depends(get_db),
):
    """
    Get all random website settings

    **Request:** No request body required

    **Response:**
    ```json
    [
        {
            "id": 1,
            "setting_name": "visit_duration_min",
            "setting_value": "30",
            "description": "Minimum time to spend on random websites (seconds)",
            "is_active": true,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "setting_name": "visit_duration_max",
            "setting_value": "120",
            "description": "Maximum time to spend on random websites (seconds)",
            "is_active": true,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ]
    ```
    """
    items, _ = random_website_settings.get_multi(
        db, skip=0, limit=None, is_active=None, search=None
    )

    return items


# ================================
# SPAM HANDLER DATA ENDPOINTS
# ================================


@router.post("/spam-handler-data", response_model=SpamHandlerDataResponse)
async def create_spam_handler_data(
    spam_data: SpamHandlerDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new spam handler data entry

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
        "timestamp": "2025-07-13T10:30:00Z",
        "created_at": "2025-07-13T10:30:00Z",
        "updated_at": "2025-07-13T10:30:00Z"
    }
    ```
    """
    return spam_handler_data.create(db, obj_in=spam_data)


# ================================
# EMAIL PROCESSING DATA ENDPOINTS
# ================================


@router.post("/email-processing-data", response_model=EmailProcessingDataResponse)
async def create_email_processing_data(
    email_data: EmailProcessingDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new email processing data entry

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

    **Note:** Fields `random_website_duration_seconds` and `total_duration_seconds` can be null or omitted.

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
        "timestamp": "2025-07-13T10:30:00Z",
        "created_at": "2025-07-13T10:30:00Z",
        "updated_at": "2025-07-13T10:30:00Z"
    }
    ```
    """
    return email_processing_data.create(db, obj_in=email_data)


# ================================
# ANALYTICS AND STATS ENDPOINTS
# ================================


@router.get("/analytics/spam-handler-stats")
async def get_spam_handler_analytics(
    db: Session = Depends(get_db),
    date_from: Optional[datetime] = Query(
        None, description="Filter from date (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None, description="Filter to date (ISO format)"
    ),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
):
    """
    Get spam handler analytics and statistics

    **Request Parameters:**
    - date_from: Filter from date in ISO format (optional)
    - date_to: Filter to date in ISO format (optional)
    - agent_name: Filter by agent name (optional)

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
    """
    stats = spam_handler_data.get_analytics(
        db, date_from=date_from, date_to=date_to, agent_name=agent_name
    )
    return stats


@router.get("/analytics/email-processing-stats")
async def get_email_processing_analytics(
    db: Session = Depends(get_db),
    date_from: Optional[datetime] = Query(
        None, description="Filter from date (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None, description="Filter to date (ISO format)"
    ),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
):
    """
    Get email processing analytics and statistics

    **Request Parameters:**
    - date_from: Filter from date in ISO format (optional)
    - date_to: Filter to date in ISO format (optional)
    - agent_name: Filter by agent name (optional)

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
    """
    stats = email_processing_data.get_analytics(
        db, date_from=date_from, date_to=date_to, agent_name=agent_name
    )
    return stats


# ================================
# PROXY ERROR ENDPOINTS
# ================================


@router.post(
    "/proxy-errors",
    response_model=ProxyErrorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_proxy_error(
    *,
    db: Session = Depends(get_db),
    proxy_error_in: ProxyErrorCreate,
) -> ProxyErrorResponse:
    """
    Create a new proxy error record.

    **Request Body:**
    ```json
    {
        "agent_name": "agent_001",
        "proxy": "192.168.1.100:8080",
        "error_details": "Connection timeout after 30 seconds",
        "profile_name": "profile_gmail_001"
    }
    ```

    **Response:**
    Returns the created proxy error record with ID and timestamps.
    """
    return proxy_error.create(db=db, obj_in=proxy_error_in)


# ================================
# LOGGED OUT PROFILE ENDPOINTS
# ================================


@router.post("/logged-out-profiles", response_model=LoggedOutProfileResponse)
async def create_logged_out_profile(
    logged_out_profile_data: LoggedOutProfileCreate,
    db: Session = Depends(get_db),
):
    """
    Create new logged out profile entry

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

    **Note:** The timestamp is automatically generated when the data is posted.
    """
    return logged_out_profile.create(db, obj_in=logged_out_profile_data)


# ================================
# HEALTH CHECK ENDPOINTS
# ================================


@router.get("/health")
async def gmail_automation_health_check():
    """
    Health check endpoint for Gmail automation APIs

    **Response:**
    ```json
    {
        "status": "healthy",
        "service": "Gmail Handler Automation API",
        "timestamp": "2025-07-13T10:30:00Z"
    }
    ```
    """
    return {
        "status": "healthy",
        "service": "Gmail Handler Automation API",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
