import smtplib
import secrets
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings


def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)


def create_verification_link(token: str) -> str:
    """Create verification link"""
    frontend_url = settings.FRONTEND_URL
    return f"{frontend_url}/verify-email?token={token}"


def create_reset_password_link(token: str) -> str:
    """Create password reset link"""
    frontend_url = settings.FRONTEND_URL
    return f"{frontend_url}/reset-password?token={token}"


def send_email(
    to_email: str, subject: str, html_content: str, text_content: str = None
) -> bool:
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email

        # Add text content if provided
        if text_content:
            part1 = MIMEText(text_content, "plain")
            msg.attach(part1)

        # Add HTML content
        part2 = MIMEText(html_content, "html")
        msg.attach(part2)

        # Connect to server and send email
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        if settings.SMTP_TLS:
            server.starttls()

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_verification_email(
    to_email: str, username: str, verification_link: str
) -> bool:
    """Send email verification email"""
    subject = "Verify Your Email - Gmail Automation Dashboard"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1a1a1a; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background: #4f46e5; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 20px 0;
            }}
            .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Gmail Automation Dashboard</h1>
            </div>
            <div class="content">
                <h2>Welcome, {username}!</h2>
                <p>Thank you for registering with Gmail Automation Dashboard. To complete your registration and access your account, please verify your email address.</p>
                
                <p style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Your Email</a>
                </p>
                
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #4f46e5;">{verification_link}</p>
                
                <p><strong>Important:</strong> This verification link will expire in 24 hours.</p>
                
                <p>If you didn't create an account with us, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>Gmail Automation Dashboard &copy; 2025</p>
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Welcome to Gmail Automation Dashboard!
    
    Thank you for registering, {username}!
    
    Please verify your email address by clicking the following link:
    {verification_link}
    
    This verification link will expire in 24 hours.
    
    If you didn't create an account with us, please ignore this email.
    
    Gmail Automation Dashboard
    """

    return send_email(to_email, subject, html_content, text_content)


def send_password_reset_email(to_email: str, username: str, reset_link: str) -> bool:
    """Send password reset email"""
    subject = "Password Reset - Gmail Automation Dashboard"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1a1a1a; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background: #ef4444; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 20px 0;
            }}
            .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Gmail Automation Dashboard</h1>
            </div>
            <div class="content">
                <h2>Password Reset Request</h2>
                <p>Hello {username},</p>
                <p>We received a request to reset your password for your Gmail Automation Dashboard account.</p>
                
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Your Password</a>
                </p>
                
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #ef4444;">{reset_link}</p>
                
                <p><strong>Important:</strong> This password reset link will expire in 1 hour.</p>
                
                <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            </div>
            <div class="footer">
                <p>Gmail Automation Dashboard &copy; 2025</p>
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Password Reset Request - Gmail Automation Dashboard
    
    Hello {username},
    
    We received a request to reset your password for your Gmail Automation Dashboard account.
    
    Please reset your password by clicking the following link:
    {reset_link}
    
    This password reset link will expire in 1 hour.
    
    If you didn't request a password reset, please ignore this email.
    
    Gmail Automation Dashboard
    """

    return send_email(to_email, subject, html_content, text_content)


def get_token_expiry(hours: int = 24) -> datetime:
    """Get token expiry datetime"""
    return datetime.utcnow() + timedelta(hours=hours)
