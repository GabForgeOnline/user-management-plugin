"""
auth.py - Authentication service for user_management plugin
Purpose: Handle user authentication, registration, password reset
Author: GabForge
Version: 1.0.0
"""

import logging
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from plugins.user_management.models import User, UserSession, EmailVerificationToken, PasswordResetToken

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
