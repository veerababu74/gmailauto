from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    users,
    clients,
    campaigns,
    default_senders,
    random_urls,
    random_website_settings,
    connectivity_settings,
    automation,
    spam_handler_data,
    email_processing_data,
    database_health,
    agents,
    agent_analytics,
    quick_actions,
    proxy_errors,
)
from app.api.endpoints import logged_out_profiles

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])

# Automation Settings APIs
api_router.include_router(
    default_senders.router, prefix="/default-senders", tags=["default-senders"]
)
api_router.include_router(
    random_urls.router, prefix="/random-urls", tags=["random-urls"]
)
api_router.include_router(
    random_website_settings.router,
    prefix="/random-website-settings",
    tags=["random-website-settings"],
)
api_router.include_router(
    connectivity_settings.router,
    prefix="/connectivity-settings",
    tags=["connectivity-settings"],
)

# Unified automation configuration API
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])

# Data Processing APIs
api_router.include_router(
    spam_handler_data.router, prefix="/spam-handler-data", tags=["spam-handler-data"]
)
api_router.include_router(
    email_processing_data.router,
    prefix="/email-processing-data",
    tags=["email-processing-data"],
)

# Database Health Check API
api_router.include_router(
    database_health.router, prefix="/database", tags=["database-health"]
)

# Agents API
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])

# Agent Analytics API
api_router.include_router(
    agent_analytics.router, prefix="/agent-analytics", tags=["agent-analytics"]
)

# Quick Actions API
api_router.include_router(
    quick_actions.router, prefix="/quick-actions", tags=["quick-actions"]
)

# Proxy Errors API
api_router.include_router(
    proxy_errors.router, prefix="/proxy-errors", tags=["proxy-errors"]
)

# Logged Out Profiles API
api_router.include_router(
    logged_out_profiles.router,
    prefix="/logged-out-profiles",
    tags=["logged-out-profiles"],
)
