from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime
from app.utils.email_validator import validate_email, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    email_notifications: bool = True

    @validator("email")
    def validate_email_field(cls, v):
        return validate_email(v)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    email_notifications: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_superuser: bool = False
    is_verified: bool = False
    gmail_connected: bool = False
    two_factor_enabled: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_superuser: bool = False
    is_verified: bool = False
    gmail_connected: bool = False
    two_factor_enabled: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_verified: bool = False
    gmail_connected: bool = False
    email_notifications: bool = True
    two_factor_enabled: bool = False
    created_at: datetime

    class Config:
        orm_mode = True


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationResponse(BaseModel):
    message: str
    email: EmailStr


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    message: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr
