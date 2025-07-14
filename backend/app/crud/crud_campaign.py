from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.schemas.campaign import CampaignStatus, CampaignType


class CRUDCampaign(CRUDBase[Campaign, CampaignCreate, CampaignUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Campaign]:
        return (
            db.query(Campaign)
            .filter(Campaign.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
        self, db: Session, *, obj_in: CampaignCreate, user_id: int
    ) -> Campaign:
        obj_in_data = obj_in.dict()
        obj_in_data["user_id"] = user_id
        db_obj = Campaign(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_status(
        self,
        db: Session,
        *,
        user_id: int,
        status: CampaignStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Campaign]:
        return (
            db.query(Campaign)
            .filter(Campaign.user_id == user_id, Campaign.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self,
        db: Session,
        *,
        user_id: int,
        campaign_type: CampaignType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Campaign]:
        return (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id, Campaign.campaign_type == campaign_type
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_stats(self, db: Session, *, user_id: int) -> dict:
        total = db.query(Campaign).filter(Campaign.user_id == user_id).count()

        active = (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id,
                Campaign.status.in_([CampaignStatus.RUNNING, CampaignStatus.SCHEDULED]),
            )
            .count()
        )

        completed = (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id, Campaign.status == CampaignStatus.COMPLETED
            )
            .count()
        )

        draft = (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id, Campaign.status == CampaignStatus.DRAFT
            )
            .count()
        )

        # Calculate totals for email metrics
        campaigns = db.query(Campaign).filter(Campaign.user_id == user_id).all()

        total_sent = sum(campaign.sent_count for campaign in campaigns)
        total_opens = sum(campaign.opened_count for campaign in campaigns)
        total_replies = sum(campaign.replied_count for campaign in campaigns)

        open_rate = (total_opens / total_sent * 100) if total_sent > 0 else 0
        reply_rate = (total_replies / total_sent * 100) if total_sent > 0 else 0

        return {
            "total_campaigns": total,
            "active_campaigns": active,
            "completed_campaigns": completed,
            "draft_campaigns": draft,
            "total_emails_sent": total_sent,
            "total_opens": total_opens,
            "total_replies": total_replies,
            "open_rate": round(open_rate, 2),
            "reply_rate": round(reply_rate, 2),
        }

    def update_metrics(
        self,
        db: Session,
        *,
        campaign_id: int,
        sent_count: Optional[int] = None,
        opened_count: Optional[int] = None,
        replied_count: Optional[int] = None
    ) -> Optional[Campaign]:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            return None

        if sent_count is not None:
            campaign.sent_count = sent_count
        if opened_count is not None:
            campaign.opened_count = opened_count
        if replied_count is not None:
            campaign.replied_count = replied_count

        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign

    def search(
        self, db: Session, *, user_id: int, query: str, skip: int = 0, limit: int = 100
    ) -> List[Campaign]:
        return (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id,
                (Campaign.name.contains(query) | Campaign.subject.contains(query)),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


campaign = CRUDCampaign(Campaign)
