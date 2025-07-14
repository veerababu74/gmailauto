from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.deps import get_db
from app.crud.crud_email_processing_data import email_processing_data
from app.crud.crud_spam_handler_data import spam_handler_data

router = APIRouter()


@router.get("/email-statistics/{agent_name}")
def get_agent_email_statistics(
    agent_name: str,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for statistics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
):
    """
    Get email statistics for a specific agent
    """
    try:
        # Get email processing data for the agent
        items, total = email_processing_data.get_multi(
            db,
            skip=0,
            limit=10000,  # Get all records for accurate statistics
            agent_name=agent_name,
            start_date=start_date,
            end_date=end_date,
        )

        if not items:
            return {
                "total_emails": 0,
                "success_rate": 0,
                "open_rate": 0,
                "click_rate": 0,
                "error_rate": 0,
                "average_duration": 0,
                "emails_opened": 0,
                "emails_clicked": 0,
                "emails_failed": 0,
                "top_recipients": [],
                "status_distribution": [],
                "popular_subjects": [],
            }

        # Calculate basic statistics
        total_emails = len(items)
        emails_opened = sum(1 for item in items if item.is_opened)
        emails_clicked = sum(1 for item in items if item.is_link_clicked)
        emails_failed = sum(1 for item in items if item.error_occurred)
        emails_successful = total_emails - emails_failed

        total_duration = sum(item.total_duration_seconds or 0 for item in items)
        avg_duration = total_duration / total_emails if total_emails > 0 else 0

        # Calculate rates
        success_rate = (
            (emails_successful / total_emails * 100) if total_emails > 0 else 0
        )
        open_rate = (emails_opened / total_emails * 100) if total_emails > 0 else 0
        click_rate = (emails_clicked / total_emails * 100) if total_emails > 0 else 0
        error_rate = (emails_failed / total_emails * 100) if total_emails > 0 else 0

        # Get top recipients (using sender_email as recipient for outgoing emails)
        recipient_counts = {}
        for item in items:
            if item.sender_email:
                recipient_counts[item.sender_email] = (
                    recipient_counts.get(item.sender_email, 0) + 1
                )

        top_recipients = [
            {"email": email, "count": count}
            for email, count in sorted(
                recipient_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        # Get status distribution
        status_counts = {
            "Sent": 0,
            "Opened": 0,
            "Clicked": 0,
            "Unsubscribed": 0,
            "Error": 0,
        }

        for item in items:
            if item.error_occurred:
                status_counts["Error"] += 1
            elif item.is_unsubscribe_clicked:
                status_counts["Unsubscribed"] += 1
            elif item.is_link_clicked:
                status_counts["Clicked"] += 1
            elif item.is_opened:
                status_counts["Opened"] += 1
            else:
                status_counts["Sent"] += 1

        status_distribution = [
            {"status": status, "count": count}
            for status, count in status_counts.items()
            if count > 0
        ]

        # Get popular subjects
        subject_counts = {}
        for item in items:
            if item.email_subject:
                subject_counts[item.email_subject] = (
                    subject_counts.get(item.email_subject, 0) + 1
                )

        popular_subjects = [
            {"subject": subject, "count": count}
            for subject, count in sorted(
                subject_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        return {
            "total_emails": total_emails,
            "success_rate": success_rate,
            "open_rate": open_rate,
            "click_rate": click_rate,
            "error_rate": error_rate,
            "average_duration": avg_duration,
            "emails_opened": emails_opened,
            "emails_clicked": emails_clicked,
            "emails_failed": emails_failed,
            "top_recipients": top_recipients,
            "status_distribution": status_distribution,
            "popular_subjects": popular_subjects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating email statistics: {str(e)}"
        )


@router.get("/spam-statistics/{agent_name}")
def get_agent_spam_statistics(
    agent_name: str,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for statistics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
):
    """
    Get spam statistics for a specific agent
    """
    try:
        # Get spam handler data for the agent
        items, total = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=10000,  # Get all records for accurate statistics
            agent_name=agent_name,
            start_date=start_date,
            end_date=end_date,
        )

        if not items:
            return {
                "total_operations": 0,
                "total_spam_found": 0,
                "total_moved_to_inbox": 0,
                "success_rate": 0,
                "error_rate": 0,
                "average_processing_time": 0,
                "operations_failed": 0,
                "top_senders": [],
                "operations_by_profile": [],
                "common_spam_subjects": [],
            }

        # Calculate basic statistics
        total_operations = len(items)
        total_spam_found = sum(item.spam_emails_found or 0 for item in items)
        total_moved_to_inbox = sum(item.moved_to_inbox or 0 for item in items)
        operations_failed = sum(1 for item in items if item.error_occurred)
        operations_successful = total_operations - operations_failed

        total_processing_time = sum(item.total_time_seconds or 0 for item in items)
        avg_processing_time = (
            total_processing_time / total_operations if total_operations > 0 else 0
        )

        # Calculate rates
        success_rate = (
            (operations_successful / total_operations * 100)
            if total_operations > 0
            else 0
        )
        error_rate = (
            (operations_failed / total_operations * 100) if total_operations > 0 else 0
        )

        # Get top spam senders
        sender_counts = {}
        for item in items:
            if (
                item.sender_email
                and item.spam_emails_found
                and item.spam_emails_found > 0
            ):
                sender_counts[item.sender_email] = (
                    sender_counts.get(item.sender_email, 0) + item.spam_emails_found
                )

        top_senders = [
            {"sender_email": sender, "count": count}
            for sender, count in sorted(
                sender_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        # Get operations by profile
        profile_counts = {}
        for item in items:
            if item.profile_name:
                profile_counts[item.profile_name] = (
                    profile_counts.get(item.profile_name, 0) + 1
                )

        operations_by_profile = [
            {"profile_name": profile, "count": count}
            for profile, count in sorted(
                profile_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        # Get common spam subjects
        subject_counts = {}
        for item in items:
            if item.spam_email_subjects:
                for subject in item.spam_email_subjects:
                    if subject:
                        subject_counts[subject] = subject_counts.get(subject, 0) + 1

        common_spam_subjects = [
            {"subject": subject, "count": count}
            for subject, count in sorted(
                subject_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        return {
            "total_operations": total_operations,
            "total_spam_found": total_spam_found,
            "total_moved_to_inbox": total_moved_to_inbox,
            "success_rate": success_rate,
            "error_rate": error_rate,
            "average_processing_time": avg_processing_time,
            "operations_failed": operations_failed,
            "top_senders": top_senders,
            "operations_by_profile": operations_by_profile,
            "common_spam_subjects": common_spam_subjects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating spam statistics: {str(e)}"
        )


@router.get("/combined-analytics/{agent_name}")
def get_agent_combined_analytics(
    agent_name: str,
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for analytics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for analytics"),
):
    """
    Get combined email and spam analytics for a specific agent
    """
    try:
        email_stats = get_agent_email_statistics(agent_name, db, start_date, end_date)
        spam_stats = get_agent_spam_statistics(agent_name, db, start_date, end_date)

        return {
            "agent_name": agent_name,
            "email_analytics": email_stats,
            "spam_analytics": spam_stats,
            "date_range": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching combined analytics: {str(e)}"
        )
