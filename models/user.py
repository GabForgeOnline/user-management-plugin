"""
user.py - User Management Plugin Models
Purpose: User, Role, Permission models with RBAC support for plugin
Author: GabForge
Version: 2.0.0 (Phase 2.1 - User Management Plugin)
"""

from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, 
    Enum as SQLEnum, ForeignKey, Table, Text, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, Enum):
    """Legacy user role enumeration (kept for backward compatibility)"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"


# ============================================================================
# ASSOCIATION TABLES (Many-to-Many)
# ============================================================================

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('assigned_at', DateTime, default=func.now()),
    Column('assigned_by', Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    Column('expires_at', DateTime, nullable=True),
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
)


# ============================================================================
# CORE MODELS
# ============================================================================

class User(Base):
    """
    User database model with extended fields for Phase 2.1.
    
    Represents a user account with authentication, profile, 
    roles, and activity tracking.
    """
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Authentication
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Profile
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)

    # Tracking
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    activity_logs = relationship("UserActivityLog", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Legacy field (kept for backward compatibility)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, index=True, nullable=True)

    def get_permissions(self):
        """Get all permissions from assigned roles"""
        permissions = set()
        for role in self.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        return permissions

    def has_permission(self, permission_name: str) -> bool:
        """Check if user has specific permission"""
        return permission_name in self.get_permissions()

    def has_role(self, role_name: str) -> bool:
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)

    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.has_role('admin') or self.has_role('super_admin')

    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username


class Role(Base):
    """
    Role definition for RBAC system.
    
    System roles: admin (30), editor (20), author (10), user (0)
    Can also create custom roles.
    """
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    level = Column(Integer, default=0)  # Hierarchy level: 0=user, 10=author, 20=editor, 30=admin
    is_system = Column(Boolean, default=False)  # Cannot delete system roles
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(Base):
    """
    Permission definition for fine-grained access control.
    
    Format: "module:action" (e.g., "posts:create", "comments:delete")
    """
    __tablename__ = "permissions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    module = Column(String(50), index=True, nullable=False)  # posts, comments, users, etc.
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.name}>"


class UserSession(Base):
    """
    Track active user sessions for token management.
    """
    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    last_activity = Column(DateTime, default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")


class UserActivityLog(Base):
    """
    Audit trail for user actions and security events.
    """
    __tablename__ = "user_activity_logs"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    action = Column(String(100), index=True, nullable=False)  # login, logout, post_created, etc.
    entity_type = Column(String(50), nullable=True)  # post, comment, user, etc.
    entity_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)  # Additional data
    created_at = Column(DateTime, default=func.now(), index=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog user_id={self.user_id} action={self.action}>"


class UserPreferences(Base):
    """
    User preferences and settings.
    """
    __tablename__ = "user_preferences"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True, nullable=False)
    theme = Column(String(20), default='light')  # light, dark
    language = Column(String(10), default='en')
    timezone = Column(String(50), default='UTC')
    email_notifications = Column(Boolean, default=True)
    digest_frequency = Column(String(20), default='daily')  # daily, weekly, monthly
    two_factor_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="preferences")


class EmailVerificationToken(Base):
    """
    Email verification tokens for user registration.
    """
    __tablename__ = "email_verification_tokens"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)


class PasswordResetToken(Base):
    """
    Password reset tokens for account recovery.
    """
    __tablename__ = "password_reset_tokens"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
