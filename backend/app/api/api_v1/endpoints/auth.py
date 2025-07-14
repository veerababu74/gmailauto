from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.core.email import (
    send_verification_email,
    send_password_reset_email,
    create_verification_link,
    create_reset_password_link,
)
from app.crud import user
from app.schemas.token import Token, LoginRequest, RegisterRequest
from app.schemas.user import (
    User,
    UserCreate,
    EmailVerificationRequest,
    EmailVerificationResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetConfirm,
    ResendVerificationRequest,
)
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_obj = user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active(user_obj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_obj.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/json", response_model=Token)
def login_json(login_data: LoginRequest, db: Session = Depends(get_db)) -> Any:
    """
    JSON login endpoint
    """
    user_obj = user.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active(user_obj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_obj.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register")
def register(
    user_data: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new user account and send verification email
    """
    # Check if user already exists
    existing_user = user.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )

    # Create new user (unverified by default)
    user_create = UserCreate(
        email=user_data.email, password=user_data.password, name=user_data.name
    )
    new_user = user.create(db, obj_in=user_create)

    # Generate verification token
    verification_token = user.create_verification_token(db, user=new_user)
    verification_link = create_verification_link(verification_token)

    # Send verification email in background
    background_tasks.add_task(
        send_verification_email, new_user.email, new_user.name, verification_link
    )

    return {
        "message": "User created successfully. Please check your email to verify your account.",
        "email": new_user.email,
        "user_id": new_user.id,
    }


@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)) -> Any:
    """
    Verify user email with token
    """
    verified_user = user.verify_email(db, token=token)
    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    return {
        "message": "Email verified successfully! You can now login to your account.",
        "email": verified_user.email,
    }


@router.post("/resend-verification")
def resend_verification(
    request: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Any:
    """
    Resend verification email
    """
    user_obj = user.get_by_email(db, email=request.email)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_obj.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already verified"
        )

    # Generate new verification token
    verification_token = user.create_verification_token(db, user=user_obj)
    verification_link = create_verification_link(verification_token)

    # Send verification email in background
    background_tasks.add_task(
        send_verification_email, user_obj.email, user_obj.name, verification_link
    )

    return {"message": "Verification email sent successfully"}


@router.post("/resend-verification/me")
def resend_verification_me(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Resend verification email for current authenticated user
    """
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already verified"
        )

    # Generate new verification token
    verification_token = user.create_verification_token(db, user=current_user)
    verification_link = create_verification_link(verification_token)

    # Send verification email in background
    background_tasks.add_task(
        send_verification_email,
        current_user.email,
        current_user.name,
        verification_link,
    )

    return {"message": "Verification email sent successfully"}


@router.post("/forgot-password")
def forgot_password(
    request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Any:
    """
    Send password reset email
    """
    user_obj = user.get_by_email(db, email=request.email)
    if not user_obj:
        # Don't reveal if email exists for security
        return {"message": "If the email exists, a password reset link has been sent"}

    if not user_obj.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email first before resetting password",
        )

    # Generate password reset token
    reset_token = user.create_password_reset_token(db, user=user_obj)
    reset_link = create_reset_password_link(reset_token)

    # Send password reset email in background
    background_tasks.add_task(
        send_password_reset_email, user_obj.email, user_obj.name, reset_link
    )

    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)) -> Any:
    """
    Reset password with token
    """
    reset_user = user.reset_password(
        db, token=request.token, new_password=request.new_password
    )
    if not reset_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    return {
        "message": "Password reset successfully! You can now login with your new password.",
        "email": reset_user.email,
    }


@router.post("/test-token", response_model=User)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user information
    """
    return current_user
