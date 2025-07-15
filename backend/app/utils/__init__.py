#!/usr/bin/env python3
"""
Utility functions and classes for the Gmail automation backend
"""

from .email_validator import EmailStr, validate_email, EmailValidationError

__all__ = ["EmailStr", "validate_email", "EmailValidationError"]
