"""
run_migrations.py - Database migration runner for user_management plugin
Purpose: Create database tables from SQLAlchemy models
Author: GabForge
Version: 1.0.0
"""

import logging
from user_management.config import Base, engine
from user_management.models import (
    User, Role, Permission, UserSession,
    UserActivityLog, UserPreferences,
    EmailVerificationToken, PasswordResetToken
)

logger = logging.getLogger(__name__)


def run_migrations():
    """
    Create all database tables for user_management plugin.
    
    This function creates the following tables:
    - users
    - roles
    - permissions
    - user_roles (junction)
    - role_permissions (junction)
    - user_sessions
    - user_activity_logs
    - user_preferences
    - email_verification_tokens
    - password_reset_tokens
    """
    try:
        logger.info("🔄 Running user_management plugin migrations...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ User management migrations completed successfully!")
        logger.info("📊 Tables created:")
        logger.info("   - users")
        logger.info("   - roles")
        logger.info("   - permissions")
        logger.info("   - user_roles (junction)")
        logger.info("   - role_permissions (junction)")
        logger.info("   - user_sessions")
        logger.info("   - user_activity_logs")
        logger.info("   - user_preferences")
        logger.info("   - email_verification_tokens")
        logger.info("   - password_reset_tokens")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ User management migration failed: {str(e)}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations()
