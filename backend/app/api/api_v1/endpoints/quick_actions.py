from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import math

from app.api.deps import get_db
from app.crud.crud_email_processing_data import email_processing_data
from app.crud.crud_spam_handler_data import spam_handler_data
from app.crud.crud_agent import agent

router = APIRouter()


@router.get("/agent-error-levels")
def get_agent_error_levels(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
):
    """
    Get agents categorized by error levels (moderate/severe)
    - Moderate: Only spam handler errors
    - Severe: Both spam handler and email processing errors
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get all agents
        all_agents_result = agent.get_multi(db, skip=0, limit=1000)
        all_agents = (
            all_agents_result[0]
            if isinstance(all_agents_result, tuple)
            else all_agents_result
        )

        moderate_agents = []
        severe_agents = []

        for agent_item in all_agents:
            # Get spam handler errors for this agent
            spam_errors, _ = spam_handler_data.get_multi(
                db,
                skip=0,
                limit=1000,
                agent_name=agent_item.agent_name,
                error_occurred=True,
                start_date=start_date,
                end_date=end_date,
            )

            # Get email processing errors for this agent
            email_errors, _ = email_processing_data.get_multi(
                db,
                skip=0,
                limit=1000,
                agent_name=agent_item.agent_name,
                error_occurred=True,
                start_date=start_date,
                end_date=end_date,
            )

            spam_error_count = len(spam_errors)
            email_error_count = len(email_errors)

            if spam_error_count > 0 or email_error_count > 0:
                agent_data = {
                    "id": agent_item.id,
                    "name": agent_item.agent_name,
                    "email": f"{agent_item.agent_name}@example.com",
                    "profile_name": agent_item.agent_name,
                    "status": "active" if agent_item.is_active else "inactive",
                    "spam_error_count": spam_error_count,
                    "email_error_count": email_error_count,
                    "total_errors": spam_error_count + email_error_count,
                    "last_error_time": None,
                    "created_at": agent_item.created_at,
                    "updated_at": agent_item.updated_at,
                }

                # Find the most recent error timestamp
                all_errors = spam_errors + email_errors
                if all_errors:
                    most_recent_error = max(all_errors, key=lambda x: x.timestamp)
                    agent_data["last_error_time"] = most_recent_error.timestamp

                # Categorize agent with time-period aware logic
                total_errors = spam_error_count + email_error_count

                # Dynamic thresholds based on time period
                # Scale thresholds based on time filter to avoid all agents being "severe" for longer periods
                if time_filter <= 24:  # 24 hours
                    severe_threshold = 15
                    moderate_threshold = 5
                    spam_severe_threshold = 8
                    email_severe_threshold = 8
                elif time_filter <= 168:  # 7 days
                    severe_threshold = 35  # ~5 errors per day
                    moderate_threshold = 10  # ~1.5 errors per day
                    spam_severe_threshold = 15
                    email_severe_threshold = 15
                else:  # 30 days and beyond
                    severe_threshold = 50  # ~1.7 errors per day
                    moderate_threshold = 15  # ~0.5 errors per day
                    spam_severe_threshold = 25
                    email_severe_threshold = 25

                # More nuanced categorization with time-aware thresholds:
                # Severe: High error count OR both types with significant counts
                # Moderate: Medium error count OR any errors below severe threshold
                if total_errors >= severe_threshold or (
                    spam_error_count >= spam_severe_threshold
                    and email_error_count >= email_severe_threshold
                ):
                    # High error volume or significant errors in both categories = Severe
                    severe_agents.append(agent_data)
                elif total_errors >= moderate_threshold or (
                    spam_error_count > 0 or email_error_count > 0
                ):
                    # Medium error volume or any errors = Moderate
                    moderate_agents.append(agent_data)

        # Sort by error count (descending) and then by last error time (most recent first)
        moderate_agents.sort(
            key=lambda x: (-x["total_errors"], x["last_error_time"] or datetime.min),
            reverse=True,
        )
        severe_agents.sort(
            key=lambda x: (-x["total_errors"], x["last_error_time"] or datetime.min),
            reverse=True,
        )

        return {
            "moderate_agents": moderate_agents,
            "severe_agents": severe_agents,
            "time_filter_hours": time_filter,
            "total_moderate": len(moderate_agents),
            "total_severe": len(severe_agents),
            "query_time": end_date.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching agent error levels: {str(e)}"
        )


@router.get("/agent-error-details/{agent_name}")
def get_agent_error_details(
    agent_name: str,
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
    error_type: Optional[str] = Query(
        None, description="Filter by error type: 'spam', 'email', or 'all'"
    ),
):
    """
    Get detailed error information for a specific agent
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get spam handler errors
        spam_errors, spam_total = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=1000,
            agent_name=agent_name,
            error_occurred=True,
            start_date=start_date,
            end_date=end_date,
        )

        # Get email processing errors
        email_errors, email_total = email_processing_data.get_multi(
            db,
            skip=0,
            limit=1000,
            agent_name=agent_name,
            error_occurred=True,
            start_date=start_date,
            end_date=end_date,
        )

        # Format spam errors
        spam_error_details = []
        for error in spam_errors:
            spam_error_details.append(
                {
                    "id": error.id,
                    "type": "spam_handler",
                    "timestamp": error.timestamp,
                    "error_details": error.error_details,
                    "profile_name": error.profile_name,
                    "sender_email": error.sender_email,
                    "spam_emails_found": error.spam_emails_found,
                    "moved_to_inbox": error.moved_to_inbox,
                    "total_time_seconds": error.total_time_seconds,
                    "created_at": error.created_at,
                }
            )

        # Format email processing errors
        email_error_details = []
        for error in email_errors:
            email_error_details.append(
                {
                    "id": error.id,
                    "type": "email_processing",
                    "timestamp": error.timestamp,
                    "error_details": error.error_details,
                    "profile_name": error.profile_name,
                    "sender_email": error.sender_email,
                    "email_subject": error.email_subject,
                    "is_opened": error.is_opened,
                    "is_link_clicked": error.is_link_clicked,
                    "is_unsubscribe_clicked": error.is_unsubscribe_clicked,
                    "is_reply_sent": error.is_reply_sent,
                    "total_duration_seconds": error.total_duration_seconds,
                    "created_at": error.created_at,
                }
            )

        # Combine and sort all errors by timestamp (most recent first)
        all_errors = spam_error_details + email_error_details
        all_errors.sort(key=lambda x: x["timestamp"], reverse=True)

        # Filter by error type if specified
        if error_type == "spam":
            filtered_errors = spam_error_details
        elif error_type == "email":
            filtered_errors = email_error_details
        else:
            filtered_errors = all_errors

        # Calculate error analytics
        total_errors = len(all_errors)
        spam_errors_count = len(spam_error_details)
        email_errors_count = len(email_error_details)

        # Error frequency analysis
        error_by_hour = {}
        for error in all_errors:
            hour_key = error["timestamp"].strftime("%Y-%m-%d %H:00")
            error_by_hour[hour_key] = error_by_hour.get(hour_key, 0) + 1

        # Most common error types
        error_patterns = {}
        for error in all_errors:
            if error["error_details"]:
                # Extract first few words as error pattern
                pattern = " ".join(error["error_details"].split()[:5])
                error_patterns[pattern] = error_patterns.get(pattern, 0) + 1

        # Sort patterns by frequency
        common_patterns = sorted(
            error_patterns.items(), key=lambda x: x[1], reverse=True
        )[:5]

        return {
            "agent_name": agent_name,
            "time_filter_hours": time_filter,
            "error_analytics": {
                "total_errors": total_errors,
                "spam_errors_count": spam_errors_count,
                "email_errors_count": email_errors_count,
                "error_rate_per_hour": (
                    total_errors / time_filter if time_filter > 0 else 0
                ),
                "error_distribution": {
                    "spam_handler": spam_errors_count,
                    "email_processing": email_errors_count,
                },
                "hourly_distribution": error_by_hour,
                "common_error_patterns": common_patterns,
            },
            "error_details": filtered_errors,
            "spam_errors": spam_error_details,
            "email_errors": email_error_details,
            "query_time": end_date.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching agent error details: {str(e)}"
        )


@router.get("/error-summary")
def get_error_summary(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
):
    """
    Get overall error summary across all agents
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get all spam handler errors
        spam_errors, spam_total = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=10000,
            error_occurred=True,
            start_date=start_date,
            end_date=end_date,
        )

        # Get all email processing errors
        email_errors, email_total = email_processing_data.get_multi(
            db,
            skip=0,
            limit=10000,
            error_occurred=True,
            start_date=start_date,
            end_date=end_date,
        )

        # Count affected agents
        spam_affected_agents = set(error.agent_name for error in spam_errors)
        email_affected_agents = set(error.agent_name for error in email_errors)
        all_affected_agents = spam_affected_agents | email_affected_agents

        # Agents with both types of errors (severe)
        severe_agents = spam_affected_agents & email_affected_agents

        # Agents with only one type of error (moderate)
        moderate_agents = all_affected_agents - severe_agents

        return {
            "time_filter_hours": time_filter,
            "total_errors": len(spam_errors) + len(email_errors),
            "spam_errors_count": len(spam_errors),
            "email_errors_count": len(email_errors),
            "total_affected_agents": len(all_affected_agents),
            "moderate_agents_count": len(moderate_agents),
            "severe_agents_count": len(severe_agents),
            "error_rate_per_hour": (
                (len(spam_errors) + len(email_errors)) / time_filter
                if time_filter > 0
                else 0
            ),
            "query_time": end_date.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching error summary: {str(e)}"
        )


@router.get("/real-time-spam-stats")
def get_real_time_spam_stats(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
    agent_name: Optional[str] = Query(
        None, description="Filter by specific agent name"
    ),
):
    """
    Get real-time spam handler statistics for Quick Actions dashboard
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get spam handler data
        spam_data, total_spam = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=10000,
            agent_name=agent_name,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate statistics
        total_processed = len(spam_data)
        spam_detected = sum(item.spam_emails_found for item in spam_data)
        errors_occurred = len([item for item in spam_data if item.error_occurred])

        # Calculate rates
        spam_detection_rate = (
            (spam_detected / total_processed * 100) if total_processed > 0 else 0
        )
        error_rate = (
            (errors_occurred / total_processed * 100) if total_processed > 0 else 0
        )

        # Get unique agents involved
        unique_agents = list(set(item.agent_name for item in spam_data))

        # Calculate hourly breakdown
        hourly_stats = {}
        for item in spam_data:
            hour_key = item.timestamp.strftime("%Y-%m-%d %H:00")
            if hour_key not in hourly_stats:
                hourly_stats[hour_key] = {"total": 0, "spam_detected": 0, "errors": 0}
            hourly_stats[hour_key]["total"] += 1
            hourly_stats[hour_key]["spam_detected"] += item.spam_emails_found
            if item.error_occurred:
                hourly_stats[hour_key]["errors"] += 1

        # Get recent errors for display
        recent_errors = [
            {
                "id": item.id,
                "agent_name": item.agent_name,
                "timestamp": item.timestamp,
                "error_message": item.error_details,
                "spam_emails_found": item.spam_emails_found,
                "sender_email": item.sender_email,
            }
            for item in spam_data
            if item.error_occurred
        ][
            :10
        ]  # Last 10 errors

        return {
            "summary": {
                "total_processed": total_processed,
                "spam_detected": spam_detected,
                "errors_occurred": errors_occurred,
                "spam_detection_rate": round(spam_detection_rate, 2),
                "error_rate": round(error_rate, 2),
                "unique_agents": len(unique_agents),
                "time_filter_hours": time_filter,
            },
            "agents_involved": unique_agents,
            "hourly_breakdown": hourly_stats,
            "recent_errors": recent_errors,
            "query_time": end_date.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching real-time spam stats: {str(e)}"
        )


@router.get("/real-time-email-stats")
def get_real_time_email_stats(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
    agent_name: Optional[str] = Query(
        None, description="Filter by specific agent name"
    ),
):
    """
    Get real-time email processing statistics for Quick Actions dashboard
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get email processing data
        email_data, total_email = email_processing_data.get_multi(
            db,
            skip=0,
            limit=10000,
            agent_name=agent_name,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate statistics
        total_processed = len(email_data)
        emails_sent = len(
            [item for item in email_data if item.is_opened]
        )  # Assuming opened means sent successfully
        clicks_generated = len([item for item in email_data if item.is_link_clicked])
        unsubscribes = len([item for item in email_data if item.is_unsubscribe_clicked])
        errors_occurred = len([item for item in email_data if item.error_occurred])

        # Calculate rates
        email_success_rate = (
            (emails_sent / total_processed * 100) if total_processed > 0 else 0
        )
        click_rate = (clicks_generated / emails_sent * 100) if emails_sent > 0 else 0
        unsubscribe_rate = (unsubscribes / emails_sent * 100) if emails_sent > 0 else 0
        error_rate = (
            (errors_occurred / total_processed * 100) if total_processed > 0 else 0
        )

        # Get unique agents involved
        unique_agents = list(set(item.agent_name for item in email_data))

        # Calculate hourly breakdown
        hourly_stats = {}
        for item in email_data:
            hour_key = item.timestamp.strftime("%Y-%m-%d %H:00")
            if hour_key not in hourly_stats:
                hourly_stats[hour_key] = {
                    "total": 0,
                    "emails_sent": 0,
                    "clicks": 0,
                    "unsubscribes": 0,
                    "errors": 0,
                }
            hourly_stats[hour_key]["total"] += 1
            if item.is_opened:
                hourly_stats[hour_key]["emails_sent"] += 1
            if item.is_link_clicked:
                hourly_stats[hour_key]["clicks"] += 1
            if item.is_unsubscribe_clicked:
                hourly_stats[hour_key]["unsubscribes"] += 1
            if item.error_occurred:
                hourly_stats[hour_key]["errors"] += 1

        # Get recent errors for display
        recent_errors = [
            {
                "id": item.id,
                "agent_name": item.agent_name,
                "timestamp": item.timestamp,
                "error_message": item.error_details,
                "email_subject": item.email_subject,
                "sender_email": item.sender_email,
                "is_opened": item.is_opened,
            }
            for item in email_data
            if item.error_occurred
        ][
            :10
        ]  # Last 10 errors

        return {
            "summary": {
                "total_processed": total_processed,
                "emails_sent": emails_sent,
                "clicks_generated": clicks_generated,
                "unsubscribes": unsubscribes,
                "errors_occurred": errors_occurred,
                "email_success_rate": round(email_success_rate, 2),
                "click_rate": round(click_rate, 2),
                "unsubscribe_rate": round(unsubscribe_rate, 2),
                "error_rate": round(error_rate, 2),
                "unique_agents": len(unique_agents),
                "time_filter_hours": time_filter,
            },
            "agents_involved": unique_agents,
            "hourly_breakdown": hourly_stats,
            "recent_errors": recent_errors,
            "query_time": end_date.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching real-time email stats: {str(e)}"
        )


@router.get("/combined-real-time-stats")
def get_combined_real_time_stats(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
):
    """
    Get combined real-time statistics for both spam handler and email processing
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get spam handler data
        spam_data, _ = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=10000,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate spam statistics
        total_spam_processed = len(spam_data)
        spam_detected = sum(item.spam_emails_found for item in spam_data)
        spam_errors_occurred = len([item for item in spam_data if item.error_occurred])
        spam_detection_rate = (
            (spam_detected / total_spam_processed * 100)
            if total_spam_processed > 0
            else 0
        )
        spam_agents_involved = list(set(item.agent_name for item in spam_data))

        # Get email processing data
        email_data, _ = email_processing_data.get_multi(
            db,
            skip=0,
            limit=10000,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate email statistics
        total_email_processed = len(email_data)
        emails_sent = total_email_processed  # All records represent sent emails
        email_errors_occurred = len(
            [item for item in email_data if item.error_occurred]
        )
        clicks_received = sum(1 for item in email_data if item.is_opened)
        click_rate = (clicks_received / emails_sent * 100) if emails_sent > 0 else 0
        email_agents_involved = list(set(item.agent_name for item in email_data))

        # Combine key metrics
        combined_summary = {
            "spam_handler": {
                "total_processed": total_spam_processed,
                "spam_detected": spam_detected,
                "spam_detection_rate": round(spam_detection_rate, 2),
                "errors_occurred": spam_errors_occurred,
            },
            "email_processing": {
                "total_processed": total_email_processed,
                "emails_sent": emails_sent,
                "click_rate": round(click_rate, 2),
                "errors_occurred": email_errors_occurred,
            },
            "combined_metrics": {
                "total_agents_involved": len(
                    set(spam_agents_involved + email_agents_involved)
                ),
                "total_errors": spam_errors_occurred + email_errors_occurred,
                "total_processed": total_spam_processed + total_email_processed,
                "combined_error_rate": round(
                    (
                        (
                            (spam_errors_occurred + email_errors_occurred)
                            / (total_spam_processed + total_email_processed)
                            * 100
                        )
                        if (total_spam_processed + total_email_processed) > 0
                        else 0
                    ),
                    2,
                ),
            },
        }

        return {
            "summary": combined_summary,
            "query_time": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching combined real-time stats: {str(e)}"
        )


@router.get("/real-time-error-summary")
def get_real_time_error_summary(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
):
    """
    Get real-time error summary that integrates with existing UI components
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get spam handler data and errors
        spam_data, _ = spam_handler_data.get_multi(
            db,
            skip=0,
            limit=10000,
            start_date=start_date,
            end_date=end_date,
        )

        spam_errors = [item for item in spam_data if item.error_occurred]

        # Get email processing data and errors
        email_data, _ = email_processing_data.get_multi(
            db,
            skip=0,
            limit=10000,
            start_date=start_date,
            end_date=end_date,
        )

        email_errors = [item for item in email_data if item.error_occurred]

        # Count affected agents
        spam_affected_agents = set(error.agent_name for error in spam_errors)
        email_affected_agents = set(error.agent_name for error in email_errors)
        all_affected_agents = spam_affected_agents | email_affected_agents

        # Agents with both types of errors (severe)
        severe_agents = spam_affected_agents & email_affected_agents

        # Agents with only one type of error (moderate)
        moderate_agents = all_affected_agents - severe_agents

        total_errors = len(spam_errors) + len(email_errors)
        error_rate_per_hour = total_errors / time_filter if time_filter > 0 else 0

        return {
            "time_filter_hours": time_filter,
            "total_errors": total_errors,
            "spam_errors_count": len(spam_errors),
            "email_errors_count": len(email_errors),
            "total_affected_agents": len(all_affected_agents),
            "moderate_agents_count": len(moderate_agents),
            "severe_agents_count": len(severe_agents),
            "error_rate_per_hour": error_rate_per_hour,
            "query_time": end_date.isoformat(),
            "spam_detection_rate": (
                sum(item.spam_emails_found for item in spam_data) / len(spam_data)
                if spam_data
                else 0
            ),
            "email_success_rate": (
                len([item for item in email_data if item.is_opened])
                / len(email_data)
                * 100
                if email_data
                else 0
            ),
            "total_spam_processed": len(spam_data),
            "total_emails_processed": len(email_data),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching real-time error summary: {str(e)}"
        )


@router.get("/real-time-agent-errors")
def get_real_time_agent_errors(
    db: Session = Depends(get_db),
    time_filter: int = Query(
        24, description="Hours to look back (24 for 24h, 168 for 7d)"
    ),
    severity: Optional[str] = Query(
        None, description="Filter by severity: 'moderate', 'severe', or 'all'"
    ),
):
    """
    Get real-time agent error data categorized by severity for Quick Actions toggle
    """
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_filter)

        # Get all agents
        all_agents_result = agent.get_multi(db, skip=0, limit=1000)
        all_agents = (
            all_agents_result[0]
            if isinstance(all_agents_result, tuple)
            else all_agents_result
        )

        moderate_agents = []
        severe_agents = []

        for agent_item in all_agents:
            # Get spam handler errors for this agent
            spam_errors, _ = spam_handler_data.get_multi(
                db,
                skip=0,
                limit=1000,
                agent_name=agent_item.agent_name,
                error_occurred=True,
                start_date=start_date,
                end_date=end_date,
            )

            # Get email processing errors for this agent
            email_errors, _ = email_processing_data.get_multi(
                db,
                skip=0,
                limit=1000,
                agent_name=agent_item.agent_name,
                error_occurred=True,
                start_date=start_date,
                end_date=end_date,
            )

            spam_error_count = len(spam_errors)
            email_error_count = len(email_errors)

            if spam_error_count > 0 or email_error_count > 0:
                agent_data = {
                    "id": agent_item.id,
                    "name": agent_item.agent_name,
                    "email": f"{agent_item.agent_name}@example.com",  # Since email might not exist in Agent model
                    "profile_name": agent_item.agent_name,
                    "status": "active" if agent_item.is_active else "inactive",
                    "spam_error_count": spam_error_count,
                    "email_error_count": email_error_count,
                    "total_errors": spam_error_count + email_error_count,
                    "last_error_time": None,
                    "created_at": agent_item.created_at,
                    "updated_at": agent_item.updated_at,
                }

                # Find the most recent error timestamp
                all_errors = spam_errors + email_errors
                if all_errors:
                    most_recent_error = max(all_errors, key=lambda x: x.timestamp)
                    agent_data["last_error_time"] = most_recent_error.timestamp

                # Categorize agent based on real-time data with time-period aware logic
                total_errors = spam_error_count + email_error_count

                # Dynamic thresholds based on time period
                # Scale thresholds based on time filter to avoid all agents being "severe" for longer periods
                if time_filter <= 24:  # 24 hours
                    severe_threshold = 15
                    moderate_threshold = 5
                    spam_severe_threshold = 8
                    email_severe_threshold = 8
                elif time_filter <= 168:  # 7 days
                    severe_threshold = 35  # ~5 errors per day
                    moderate_threshold = 10  # ~1.5 errors per day
                    spam_severe_threshold = 15
                    email_severe_threshold = 15
                else:  # 30 days and beyond
                    severe_threshold = 50  # ~1.7 errors per day
                    moderate_threshold = 15  # ~0.5 errors per day
                    spam_severe_threshold = 25
                    email_severe_threshold = 25

                # More nuanced categorization with time-aware thresholds:
                # Severe: High error count OR both types with significant counts
                # Moderate: Medium error count OR any errors below severe threshold
                if total_errors >= severe_threshold or (
                    spam_error_count >= spam_severe_threshold
                    and email_error_count >= email_severe_threshold
                ):
                    # High error volume or significant errors in both categories = Severe
                    severe_agents.append(agent_data)
                elif total_errors >= moderate_threshold or (
                    spam_error_count > 0 or email_error_count > 0
                ):
                    # Medium error volume or any errors = Moderate
                    moderate_agents.append(agent_data)

        # Sort by error count (descending) and then by last error time (most recent first)
        moderate_agents.sort(
            key=lambda x: (-x["total_errors"], x["last_error_time"] or datetime.min),
            reverse=True,
        )
        severe_agents.sort(
            key=lambda x: (-x["total_errors"], x["last_error_time"] or datetime.min),
            reverse=True,
        )

        # Return based on severity filter
        if severity == "moderate":
            return {
                "agents": moderate_agents,
                "total_count": len(moderate_agents),
                "severity": "moderate",
                "time_filter_hours": time_filter,
                "query_time": end_date.isoformat(),
            }
        elif severity == "severe":
            return {
                "agents": severe_agents,
                "total_count": len(severe_agents),
                "severity": "severe",
                "time_filter_hours": time_filter,
                "query_time": end_date.isoformat(),
            }
        else:
            return {
                "moderate_agents": moderate_agents,
                "severe_agents": severe_agents,
                "total_moderate": len(moderate_agents),
                "total_severe": len(severe_agents),
                "time_filter_hours": time_filter,
                "query_time": end_date.isoformat(),
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching real-time agent errors: {str(e)}"
        )
