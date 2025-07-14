from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import campaign
from app.schemas.campaign import (
    Campaign,
    CampaignCreate,
    CampaignUpdate,
    CampaignStats,
    CampaignStatus,
    CampaignType,
)
from app.schemas.user import User
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Campaign])
def read_campaigns(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: CampaignStatus = Query(None, alias="status"),
    type_filter: CampaignType = Query(None, alias="type"),
    search: str = Query(None),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve campaigns for current user
    """
    if search:
        campaigns = campaign.search(
            db, user_id=current_user.id, query=search, skip=skip, limit=limit
        )
    elif status_filter:
        campaigns = campaign.get_by_status(
            db, user_id=current_user.id, status=status_filter, skip=skip, limit=limit
        )
    elif type_filter:
        campaigns = campaign.get_by_type(
            db,
            user_id=current_user.id,
            campaign_type=type_filter,
            skip=skip,
            limit=limit,
        )
    else:
        campaigns = campaign.get_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return campaigns


@router.post("/", response_model=Campaign)
def create_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_in: CampaignCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new campaign
    """
    new_campaign = campaign.create_with_user(
        db, obj_in=campaign_in, user_id=current_user.id
    )
    return new_campaign


@router.get("/stats", response_model=CampaignStats)
def read_campaign_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get campaign statistics for current user
    """
    stats = campaign.get_stats(db, user_id=current_user.id)
    return stats


@router.get("/{campaign_id}", response_model=Campaign)
def read_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get campaign by ID
    """
    campaign_obj = campaign.get(db, id=campaign_id)
    if not campaign_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )
    if campaign_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return campaign_obj


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    campaign_in: CampaignUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update campaign
    """
    campaign_obj = campaign.get(db, id=campaign_id)
    if not campaign_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )
    if campaign_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    updated_campaign = campaign.update(db, db_obj=campaign_obj, obj_in=campaign_in)
    return updated_campaign


@router.delete("/{campaign_id}")
def delete_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete campaign
    """
    campaign_obj = campaign.get(db, id=campaign_id)
    if not campaign_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )
    if campaign_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    campaign.remove(db, id=campaign_id)
    return {"message": "Campaign deleted successfully"}


@router.post("/{campaign_id}/start")
def start_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Start a campaign
    """
    campaign_obj = campaign.get(db, id=campaign_id)
    if not campaign_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )
    if campaign_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )

    # Update campaign status to running
    updated_campaign = campaign.update(
        db, db_obj=campaign_obj, obj_in={"status": CampaignStatus.RUNNING}
    )
    return {"message": "Campaign started successfully", "campaign": updated_campaign}


@router.post("/{campaign_id}/pause")
def pause_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Pause a campaign
    """
    campaign_obj = campaign.get(db, id=campaign_id)
    if not campaign_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )
    if campaign_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )

    # Update campaign status to paused
    updated_campaign = campaign.update(
        db, db_obj=campaign_obj, obj_in={"status": CampaignStatus.PAUSED}
    )
    return {"message": "Campaign paused successfully", "campaign": updated_campaign}
