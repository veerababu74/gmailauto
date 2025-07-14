from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.crud_default_sender import default_sender
from app.crud.crud_random_url import random_url
from app.crud.crud_random_website_settings import random_website_settings
from app.crud.crud_connectivity_settings import connectivity_settings

router = APIRouter()


@router.get("/automation-config", response_model=Dict[str, Any])
def get_complete_automation_config(db: Session = Depends(get_db)):
    """
    Get complete automation configuration in a single API call
    This endpoint provides all settings needed by the automation system
    """

    # Get default senders
    default_senders_list = default_sender.get_emails_list(db, is_active=True)

    # Get random URLs
    random_urls_list = random_url.get_urls_list(db, is_active=True)

    # Get random website settings
    random_website_config = random_website_settings.get_config_dict(db)

    # Get connectivity settings
    connectivity_config = connectivity_settings.get_config_dict(db)

    return {
        "DEFAULT_SENDERS": default_senders_list,
        "RANDOM_URLS": random_urls_list,
        **random_website_config,
        **connectivity_config,
        "api_version": "1.0",
        "last_updated": None,  # You can add timestamp tracking later
    }


@router.get("/automation-config/default-senders")
def get_automation_default_senders(db: Session = Depends(get_db)):
    """
    Get default senders for automation (compatible with existing API client)
    """
    return {"DEFAULT_SENDERS": default_sender.get_emails_list(db, is_active=True)}


@router.get("/automation-config/random-urls")
def get_automation_random_urls(db: Session = Depends(get_db)):
    """
    Get random URLs for automation (compatible with existing API client)
    """
    return {"RANDOM_URLS": random_url.get_urls_list(db, is_active=True)}


@router.get("/automation-config/random-website")
def get_automation_random_website_settings(db: Session = Depends(get_db)):
    """
    Get random website settings for automation (compatible with existing API client)
    """
    return random_website_settings.get_config_dict(db)


@router.get("/automation-config/connectivity")
def get_automation_connectivity_settings(db: Session = Depends(get_db)):
    """
    Get connectivity settings for automation (compatible with existing API client)
    """
    return connectivity_settings.get_config_dict(db)


@router.post("/automation-config/initialize")
def initialize_automation_settings(db: Session = Depends(get_db)):
    """
    Initialize all automation settings with default values
    """

    # Initialize random website settings
    random_website_defaults = random_website_settings.initialize_default_settings(db)

    # Initialize connectivity settings
    connectivity_defaults = connectivity_settings.initialize_default_settings(db)

    # Initialize some default URLs if none exist
    if not random_url.get_active(db):
        default_urls = [
            {
                "url": "https://www.instagram.com",
                "category": "social",
                "description": "Instagram",
            },
            {
                "url": "https://www.facebook.com",
                "category": "social",
                "description": "Facebook",
            },
            {
                "url": "https://www.youtube.com",
                "category": "entertainment",
                "description": "YouTube",
            },
            {
                "url": "https://www.flipkart.com",
                "category": "shopping",
                "description": "Flipkart",
            },
            {
                "url": "https://www.amazon.in",
                "category": "shopping",
                "description": "Amazon India",
            },
            {"url": "https://www.ndtv.com", "category": "news", "description": "NDTV"},
            {
                "url": "https://www.cricbuzz.com",
                "category": "sports",
                "description": "Cricbuzz",
            },
            {
                "url": "https://www.linkedin.com",
                "category": "social",
                "description": "LinkedIn",
            },
            {
                "url": "https://www.github.com",
                "category": "technology",
                "description": "GitHub",
            },
            {
                "url": "https://www.stackoverflow.com",
                "category": "technology",
                "description": "Stack Overflow",
            },
        ]

        from app.schemas.random_url import RandomUrlCreate

        for url_data in default_urls:
            url_create = RandomUrlCreate(**url_data)
            random_url.create(db, obj_in=url_create)

    # Initialize a default sender if none exist
    if not default_sender.get_active(db):
        from app.schemas.default_sender import DefaultSenderCreate

        default_email = DefaultSenderCreate(
            email="info@findexco.com",
            description="Default sender email",
            is_active=True,
        )
        default_sender.create(db, obj_in=default_email)

    return {
        "message": "Automation settings initialized successfully",
        "random_website_settings_created": len(random_website_defaults),
        "connectivity_settings_created": len(connectivity_defaults),
    }


@router.get("/health")
def automation_api_health():
    """
    Health check for automation API
    """
    return {
        "status": "healthy",
        "message": "Automation API is running",
        "endpoints": [
            "/automation-config",
            "/automation-config/default-senders",
            "/automation-config/random-urls",
            "/automation-config/random-website",
            "/automation-config/connectivity",
        ],
    }
