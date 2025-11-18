"""
User Management Plugin - Independent RBAC System
Version: 1.0.0
Author: GabForge Team

This is a standalone plugin that can be used across multiple platforms.
It provides:
- User registration and authentication
- Role-based access control (RBAC)
- Permission management
- Activity logging and audit trail
- User profiles and preferences

Plugin can be disabled without affecting main application.
"""

from typing import Dict, Any, Optional
from .models import User, Role, Permission
from .services.auth import AuthService
from .services.rbac import RBACService

__version__ = "1.0.0"
__author__ = "GabForge Team"
__all__ = ["UserManagementPlugin", "get_plugin_info"]


class UserManagementPlugin:
    """
    User Management Plugin for GabForge platform.
    
    This plugin is independent and can be used as a standalone module
    or integrated into the main application.
    """
    
    name = "user_management"
    version = "1.0.0"
    description = "User authentication, RBAC, and activity logging"
    enabled = True
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the plugin with optional configuration."""
        self.config = config or {}
        self.auth_service = AuthService()
        self.rbac_service = RBACService()
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled,
            "models": ["User", "Role", "Permission", "UserSession", "UserActivityLog"],
            "services": ["AuthService", "RBACService"],
        }
    
    def initialize(self) -> bool:
        """Initialize the plugin (create tables, seed data)."""
        try:
            from .migrations import run_migrations
            from .migrations import seed_roles_and_permissions
            
            run_migrations()
            seed_roles_and_permissions()
            return True
        except Exception as e:
            print(f"Error initializing user_management plugin: {e}")
            return False
    
    def get_models(self):
        """Get all plugin models for registration."""
        return [User, Role, Permission]
    
    def get_routes(self):
        """Get all plugin API routes."""
        try:
            from .api.routes import auth, users, admin
            return [auth.router, users.router, admin.router]
        except Exception as e:
            print(f"Error loading routes: {e}")
            return []


def get_plugin_info() -> Dict[str, Any]:
    """Get plugin information (called by plugin manager)."""
    return {
        "name": "user_management",
        "version": "1.0.0",
        "class": UserManagementPlugin,
        "description": "User authentication, RBAC, and activity logging",
    }
