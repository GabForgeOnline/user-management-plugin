"""
auth.py - Authentication service for user_management plugin
Purpose: Handle user authentication, registration, password reset, JWT tokens
Author: GabForge
Version: 1.0.0
"""

import logging
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from user_management.models import User, UserSession, EmailVerificationToken, PasswordResetToken
from user_management.config import get_db, settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme for Bearer token
security = HTTPBearer()


class AuthService:
    """Authentication service for user_management plugin"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, hashed)
    
    @staticmethod
    def create_user(db: Session, email: str, username: str, password: str, 
                   first_name: str = None, last_name: str = None) -> User:
        """Create new user"""
        hashed_password = AuthService.hash_password(password)
        
        user = User(
            email=email,
            username=username,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"✅ User created: {email}")
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate user by email and password"""
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"❌ User not found: {email}")
            return None
        
        if not AuthService.verify_password(password, user.password_hash):
            logger.warning(f"❌ Invalid password: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"❌ User inactive: {email}")
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info(f"✅ User authenticated: {email}")
        return user
    
    @staticmethod
    def change_password(db: Session, user: User, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if not AuthService.verify_password(old_password, user.password_hash):
            logger.warning(f"❌ Invalid old password: {user.email}")
            return False
        
        user.password_hash = AuthService.hash_password(new_password)
        db.commit()
        
        logger.info(f"✅ Password changed: {user.email}")
        return True
    
    @staticmethod
    def create_access_token(user_id: int, expires_in_hours: int = None) -> str:
        """Create JWT access token"""
        if expires_in_hours is None:
            expires_in_hours = settings.JWT_EXPIRATION_HOURS
        
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def create_refresh_token(user_id: int, expires_in_days: int = None) -> str:
        """Create JWT refresh token"""
        if expires_in_days is None:
            expires_in_days = settings.JWT_REFRESH_EXPIRATION_DAYS
        
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=expires_in_days),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def verify_access_token(token: str) -> int:
        """Verify JWT access token and return user_id"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            if payload.get("type") != "access":
                logger.warning("❌ Invalid token type")
                return None
            
            user_id = int(payload.get("sub"))
            return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("❌ Invalid token")
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> int:
        """Verify JWT refresh token and return user_id"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            if payload.get("type") != "refresh":
                logger.warning("❌ Invalid token type")
                return None
            
            user_id = int(payload.get("sub"))
            return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Refresh token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("❌ Invalid refresh token")
            return None
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> User:
        """Get current authenticated user from token"""
        token = credentials.credentials
        
        user_id = AuthService.verify_access_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
