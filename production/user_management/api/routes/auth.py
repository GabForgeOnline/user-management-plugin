"""
auth_routes.py - Authentication API endpoints
Purpose: User registration, login, token refresh, logout
Author: User Management Plugin Team
Version: 1.0.0
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from user_management.config import get_db, settings
from user_management.services.auth import AuthService
from user_management.models import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    username: str
    password: str
    first_name: str = None
    last_name: str = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePassword123!",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!"
            }
        }


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    username: str
    first_name: str = None
    last_name: str = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    old_password: str
    new_password: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Email address (must be unique)
    - **username**: Username (must be unique)
    - **password**: Password (min 8 characters)
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    """
    # Check if user exists
    existing = db.query(User).filter(
        (User.email == request.email) | (User.username == request.username)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered"
        )
    
    # Validate password strength
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Create user
    user = AuthService.create_user(
        db=db,
        email=request.email,
        username=request.username,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name
    )
    
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and get authentication tokens
    
    Returns:
    - **access_token**: JWT token for API requests (expires in 24 hours by default)
    - **refresh_token**: Token for refreshing access token (expires in 7 days)
    """
    user = AuthService.authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    access_token = AuthService.create_access_token(
        user_id=user.id,
        expires_in_hours=settings.JWT_EXPIRATION_HOURS
    )
    refresh_token = AuthService.create_refresh_token(
        user_id=user.id,
        expires_in_days=settings.JWT_REFRESH_EXPIRATION_DAYS
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    Returns new access token with extended expiration
    """
    user_id = AuthService.verify_refresh_token(refresh_token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    access_token = AuthService.create_access_token(
        user_id=user.id,
        expires_in_hours=settings.JWT_EXPIRATION_HOURS
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(AuthService.get_current_user),
):
    """
    Get current authenticated user information
    
    Requires: Bearer token in Authorization header
    """
    return current_user


@router.post("/logout", status_code=204)
async def logout(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user (invalidates tokens if using blacklist)
    
    In production, implement token blacklisting with Redis
    """
    # TODO: Implement token blacklisting
    pass


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    Requires: Valid current password
    """
    if not AuthService.verify_password(request.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current password"
        )
    
    # Hash and update password
    current_user.password_hash = AuthService.hash_password(request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/password-reset-request")
async def request_password_reset(
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """
    Request password reset (sends email with reset token)
    
    In production, implement email sending
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If email exists, password reset link has been sent"}
    
    # TODO: Generate reset token and send email
    return {"message": "If email exists, password reset link has been sent"}
