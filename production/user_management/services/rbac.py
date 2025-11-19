"""
rbac.py - Role-Based Access Control service for user_management plugin
Purpose: Handle permission checks, role management, RBAC logic
Author: GabForge
Version: 1.0.0
"""

import logging
from sqlalchemy.orm import Session
from user_management.models import User, Role, Permission

logger = logging.getLogger(__name__)


class RBACService:
    """Role-Based Access Control service"""
    
    @staticmethod
    def check_permission(user: User, permission_name: str) -> bool:
        """Check if user has specific permission"""
        if not user or not user.is_active:
            return False
        
        return user.has_permission(permission_name)
    
    @staticmethod
    def check_role(user: User, role_name: str) -> bool:
        """Check if user has specific role"""
        if not user or not user.is_active:
            return False
        
        return user.has_role(role_name)
    
    @staticmethod
    def is_admin(user: User) -> bool:
        """Check if user is admin"""
        if not user or not user.is_active:
            return False
        
        return user.is_admin()
    
    @staticmethod
    def assign_role(db: Session, user: User, role_name: str, assigned_by: User = None) -> bool:
        """Assign role to user"""
        role = db.query(Role).filter(Role.name == role_name).first()
        
        if not role:
            logger.warning(f"❌ Role not found: {role_name}")
            return False
        
        if role in user.roles:
            logger.warning(f"⚠️  User already has role: {user.email} -> {role_name}")
            return False
        
        user.roles.append(role)
        db.commit()
        
        logger.info(f"✅ Role assigned: {user.email} -> {role_name}")
        return True
    
    @staticmethod
    def remove_role(db: Session, user: User, role_name: str) -> bool:
        """Remove role from user"""
        role = db.query(Role).filter(Role.name == role_name).first()
        
        if not role:
            logger.warning(f"❌ Role not found: {role_name}")
            return False
        
        if role not in user.roles:
            logger.warning(f"⚠️  User doesn't have role: {user.email} -> {role_name}")
            return False
        
        user.roles.remove(role)
        db.commit()
        
        logger.info(f"✅ Role removed: {user.email} -> {role_name}")
        return True
    
    @staticmethod
    def get_user_permissions(user: User) -> set:
        """Get all permissions for user"""
        if not user or not user.is_active:
            return set()
        
        return user.get_permissions()
    
    @staticmethod
    def get_user_roles(user: User) -> list:
        """Get all roles for user"""
        if not user or not user.is_active:
            return []
        
        return [role.name for role in user.roles]
