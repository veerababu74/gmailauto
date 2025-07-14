#!/usr/bin/env python3
"""
Add comprehensive dummy data for Agent Analytics testing
This script creates realistic test data for agents, email processing, and spam handler operations
"""

import sys
import os
import random
from datetime import datetime, timedelta
from typing import List

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(backend_dir, ".."))

from app.core.database import get_db
from app.models.agent import Agent
from app.models.email_processing_data import EmailProcessingData
from app.models.spam_handler_data import SpamHandlerData
from sqlalchemy.orm import Session


class DummyDataGenerator:
    """Generate realistic dummy data for testing"""

    def __init__(self):
        self.agents = [
            {
                "name": "Gmail-Agent-NYC-001",
                "brand": "Dell OptiPlex",
                "location": "New York Office - Floor 3",
            },
            {
                "name": "Gmail-Agent-LA-002",
                "brand": "HP EliteDesk",
                "location": "Los Angeles Office - Server Room A",
            },
            {
                "name": "Gmail-Agent-CHI-003",
                "brand": "Lenovo ThinkCentre",
                "location": "Chicago Office - IT Department",
            },
            {
                "name": "Gmail-Agent-MIA-004",
                "brand": "ASUS VivoMini",
                "location": "Miami Office - Floor 2",
            },
            {
                "name": "Gmail-Agent-SEA-005",
                "brand": "Intel NUC",
                "location": "Seattle Office - Cloud Center",
            },
            {
                "name": "Gmail-Agent-ATL-006",
                "brand": "Dell XPS",
                "location": "Atlanta Office - Main Server",
            },
            {
                "name": "Gmail-Agent-DEN-007",
                "brand": "HP ProDesk",
                "location": "Denver Office - Data Center",
            },
            {
                "name": "Gmail-Agent-PHX-008",
                "brand": "Lenovo Legion",
                "location": "Phoenix Office - Tech Hub",
            },
        ]

        self.profiles = [
            "john.doe.profile",
            "jane.smith.profile",
            "mike.johnson.profile",
            "sarah.wilson.profile",
            "david.brown.profile",
            "lisa.davis.profile",
            "chris.miller.profile",
            "amanda.garcia.profile",
            "robert.martinez.profile",
            "jessica.lopez.profile",
        ]

        self.email_subjects = [
            "Quarterly Business Review - Q4 2024",
            "Marketing Campaign Launch Update",
            "Team Meeting Scheduled for Tomorrow",
            "Project Status Report - Week 52",
            "Client Onboarding Process Complete",
            "Monthly Sales Performance Review",
            "System Maintenance Notification",
            "Welcome to Our Newsletter!",
            "Product Update - New Features Available",
            "Training Session Invitation",
            "Budget Approval Request",
            "Customer Feedback Summary",
            "Holiday Schedule Announcement",
            "Security Policy Update Required",
            "Partnership Opportunity Discussion",
            "Invoice Processing Complete",
            "Event Registration Confirmation",
            "Weekly Performance Metrics",
            "Software License Renewal",
            "Data Backup Completion Notice",
        ]

        self.spam_subjects = [
            "URGENT: Your account will be suspended!",
            "Congratulations! You've won $1,000,000!",
            "Click here for amazing weight loss pills",
            "Hot singles in your area want to meet",
            "Make money fast working from home",
            "Your computer has been infected - click now",
            "Free gift card waiting for you",
            "Enlarge your... business opportunities",
            "Nigerian Prince needs your help",
            "You have unclaimed funds waiting",
            "Miracle cure doctors don't want you to know",
            "Act now - limited time offer expires today",
            "Your package delivery failed - update info",
            "IRS tax refund pending - verify account",
            "Bitcoin investment opportunity - guaranteed returns",
        ]

        self.sender_emails = [
            "notifications@company.com",
            "support@business.org",
            "info@startup.io",
            "admin@corporation.net",
            "team@agency.com",
            "alerts@platform.co",
            "updates@service.com",
            "news@website.org",
            "contact@firm.net",
            "hello@startup.io",
            "no-reply@system.com",
            "automated@service.org",
        ]

        self.spam_senders = [
            "winner@lottery.scam",
            "urgent@bank.fake",
            "offer@pills.spam",
            "hot@singles.fake",
            "money@home.scam",
            "virus@alert.fake",
            "gift@card.spam",
            "prince@nigeria.scam",
            "cure@miracle.fake",
            "refund@irs.scam",
            "bitcoin@invest.fake",
            "delivery@failed.scam",
        ]

        self.recipient_emails = [
            "user1@testcompany.com",
            "user2@testcompany.com",
            "user3@testcompany.com",
            "manager@testcompany.com",
            "admin@testcompany.com",
            "support@testcompany.com",
            "sales@testcompany.com",
            "marketing@testcompany.com",
            "hr@testcompany.com",
            "finance@testcompany.com",
            "operations@testcompany.com",
            "dev@testcompany.com",
        ]

    def create_agents(self, db: Session):
        """Create agent records"""
        print("Creating agents...")

        for agent_data in self.agents:
            # Check if agent already exists
            existing = (
                db.query(Agent).filter(Agent.agent_name == agent_data["name"]).first()
            )
            if existing:
                print(f"Agent {agent_data['name']} already exists, skipping...")
                continue

            agent = Agent(
                agent_name=agent_data["name"],
                machine_brand=agent_data["brand"],
                location=agent_data["location"],
                is_active=random.choice(
                    [True, True, True, False]
                ),  # 75% chance of being active
                registration_date=datetime.utcnow()
                - timedelta(days=random.randint(1, 365)),
                registration_time=datetime.utcnow()
                - timedelta(days=random.randint(1, 365)),
            )
            db.add(agent)
            print(f"Created agent: {agent_data['name']}")

        db.commit()
        print(f"Successfully created {len(self.agents)} agents!")

    def create_email_processing_data(self, db: Session, records_per_agent: int = 50):
        """Create email processing data for each agent"""
        print("Creating email processing data...")

        agents = db.query(Agent).all()
        total_records = 0

        for agent in agents:
            print(f"Creating email data for agent: {agent.agent_name}")

            for i in range(records_per_agent):
                # Generate timestamp within last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)

                timestamp = datetime.utcnow() - timedelta(
                    days=days_ago, hours=hours_ago, minutes=minutes_ago
                )

                # Random email actions with realistic probabilities
                is_opened = random.random() < 0.65  # 65% open rate
                is_link_clicked = (
                    is_opened and random.random() < 0.25
                )  # 25% click rate if opened
                is_unsubscribe_clicked = (
                    is_opened and random.random() < 0.05
                )  # 5% unsubscribe if opened
                is_reply_sent = (
                    is_opened and random.random() < 0.15
                )  # 15% reply rate if opened
                error_occurred = random.random() < 0.08  # 8% error rate

                # Random durations
                random_website_duration = (
                    random.uniform(10, 300) if random.random() < 0.7 else 0
                )
                total_duration = random.uniform(30, 600)

                # Create email processing record
                email_record = EmailProcessingData(
                    agent_name=agent.agent_name,
                    profile_name=random.choice(self.profiles),
                    sender_email=random.choice(self.sender_emails),
                    email_subject=random.choice(self.email_subjects),
                    is_opened=is_opened,
                    is_link_clicked=is_link_clicked,
                    is_unsubscribe_clicked=is_unsubscribe_clicked,
                    is_reply_sent=is_reply_sent,
                    random_website_visited=(
                        f"https://example{random.randint(1,100)}.com"
                        if random_website_duration > 0
                        else None
                    ),
                    random_website_duration_seconds=random_website_duration,
                    total_duration_seconds=total_duration,
                    error_occurred=error_occurred,
                    error_details="Connection timeout" if error_occurred else None,
                    timestamp=timestamp,
                    created_at=timestamp,
                    updated_at=timestamp,
                )

                db.add(email_record)
                total_records += 1

                # Commit in batches for better performance
                if total_records % 100 == 0:
                    db.commit()
                    print(f"Committed {total_records} email records...")

        db.commit()
        print(f"Successfully created {total_records} email processing records!")

    def create_spam_handler_data(self, db: Session, records_per_agent: int = 30):
        """Create spam handler data for each agent"""
        print("Creating spam handler data...")

        agents = db.query(Agent).all()
        total_records = 0

        for agent in agents:
            print(f"Creating spam data for agent: {agent.agent_name}")

            for i in range(records_per_agent):
                # Generate timestamp within last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)

                timestamp = datetime.utcnow() - timedelta(
                    days=days_ago, hours=hours_ago, minutes=minutes_ago
                )

                # Random spam detection with realistic probabilities
                spam_found = random.randint(0, 8)  # 0-8 spam emails found
                moved_to_inbox = (
                    random.randint(0, min(spam_found, 3)) if spam_found > 0 else 0
                )  # Some false positives
                error_occurred = random.random() < 0.05  # 5% error rate

                # Select spam subjects if spam was found
                spam_subjects = []
                if spam_found > 0:
                    spam_subjects = random.sample(
                        self.spam_subjects, min(spam_found, len(self.spam_subjects))
                    )

                # Random processing time
                total_time = random.uniform(15, 180)  # 15 seconds to 3 minutes

                # Create spam handler record
                spam_record = SpamHandlerData(
                    agent_name=agent.agent_name,
                    profile_name=random.choice(self.profiles),
                    sender_email=random.choice(
                        self.spam_senders if spam_found > 0 else self.sender_emails
                    ),
                    spam_emails_found=spam_found,
                    moved_to_inbox=moved_to_inbox,
                    total_time_seconds=total_time,
                    error_occurred=error_occurred,
                    error_details="Spam filter timeout" if error_occurred else None,
                    timestamp=timestamp,
                    spam_email_subjects=spam_subjects if spam_subjects else None,
                    created_at=timestamp,
                    updated_at=timestamp,
                )

                db.add(spam_record)
                total_records += 1

                # Commit in batches for better performance
                if total_records % 100 == 0:
                    db.commit()
                    print(f"Committed {total_records} spam records...")

        db.commit()
        print(f"Successfully created {total_records} spam handler records!")

    def add_recent_data(self, db: Session):
        """Add some very recent data (last 24 hours) for real-time testing"""
        print("Adding recent data for real-time testing...")

        agents = db.query(Agent).filter(Agent.is_active == True).all()

        for agent in agents:
            # Add 5-10 recent email records
            for i in range(random.randint(5, 10)):
                timestamp = datetime.utcnow() - timedelta(
                    hours=random.randint(0, 24), minutes=random.randint(0, 59)
                )

                email_record = EmailProcessingData(
                    agent_name=agent.agent_name,
                    profile_name=random.choice(self.profiles),
                    sender_email=random.choice(self.sender_emails),
                    email_subject=f"[RECENT] {random.choice(self.email_subjects)}",
                    is_opened=random.random() < 0.7,
                    is_link_clicked=random.random() < 0.3,
                    is_unsubscribe_clicked=random.random() < 0.05,
                    is_reply_sent=random.random() < 0.2,
                    total_duration_seconds=random.uniform(30, 200),
                    error_occurred=random.random() < 0.05,
                    timestamp=timestamp,
                    created_at=timestamp,
                    updated_at=timestamp,
                )
                db.add(email_record)

            # Add 3-5 recent spam records
            for i in range(random.randint(3, 5)):
                timestamp = datetime.utcnow() - timedelta(
                    hours=random.randint(0, 24), minutes=random.randint(0, 59)
                )

                spam_found = random.randint(0, 5)
                spam_record = SpamHandlerData(
                    agent_name=agent.agent_name,
                    profile_name=random.choice(self.profiles),
                    sender_email=random.choice(
                        self.spam_senders if spam_found > 0 else self.sender_emails
                    ),
                    spam_emails_found=spam_found,
                    moved_to_inbox=(
                        random.randint(0, min(spam_found, 2)) if spam_found > 0 else 0
                    ),
                    total_time_seconds=random.uniform(20, 120),
                    error_occurred=random.random() < 0.03,
                    timestamp=timestamp,
                    spam_email_subjects=(
                        random.sample(self.spam_subjects, min(spam_found, 3))
                        if spam_found > 0
                        else None
                    ),
                    created_at=timestamp,
                    updated_at=timestamp,
                )
                db.add(spam_record)

        db.commit()
        print("Successfully added recent data!")


def main():
    """Main function to populate all dummy data"""
    print("🚀 Starting dummy data generation for Agent Analytics...")
    print("=" * 60)

    try:
        # Get database session
        db = next(get_db())

        # Initialize data generator
        generator = DummyDataGenerator()

        # Create all dummy data
        generator.create_agents(db)
        print()

        generator.create_email_processing_data(db, records_per_agent=75)
        print()

        generator.create_spam_handler_data(db, records_per_agent=50)
        print()

        generator.add_recent_data(db)
        print()

        print("=" * 60)
        print("✅ Dummy data generation completed successfully!")
        print()
        print("📊 Summary:")

        # Print summary statistics
        agent_count = db.query(Agent).count()
        email_count = db.query(EmailProcessingData).count()
        spam_count = db.query(SpamHandlerData).count()

        print(f"   • Agents: {agent_count}")
        print(f"   • Email Processing Records: {email_count}")
        print(f"   • Spam Handler Records: {spam_count}")
        print()
        print("🎯 You can now test Agent Analytics with realistic data!")
        print(
            "   Navigate to Agent Analytics in the dashboard to see the data in action."
        )

        db.close()

    except Exception as e:
        print(f"❌ Error generating dummy data: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
