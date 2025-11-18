"""
seed_roles_and_permissions.py - Seed initial roles and permissions for user_management plugin
Purpose: Initialize system roles and permissions
Author: GabForge
Version: 1.0.0
"""

import logging
from sqlalchemy.orm import Session
from config.database import SessionLocal
from plugins.user_management.models import Role, Permission

logger = logging.getLogger(__name__)


# System Roles (predefined)
SYSTEM_ROLES = [
    {
        "name": "super_admin",
        "description": "Super administrator with full system access",
        "level": 40,
        "is_system": True,
    },
    {
        "name": "admin",
        "description": "Administrator with full access except system settings",
        "level": 30,
        "is_system": True,
    },
    {
        "name": "editor",
        "description": "Editor who can manage all content",
        "level": 20,
        "is_system": True,
    },
    {
        "name": "author",
        "description": "Author who can create and edit own content",
        "level": 10,
        "is_system": True,
    },
    {
        "name": "user",
        "description": "Regular user with basic access",
        "level": 0,
        "is_system": True,
    },
]


# Permissions by Module
PERMISSIONS = {
    "users": [
        ("users:list", "List all users"),
        ("users:create", "Create new user"),
        ("users:read", "View user details"),
        ("users:update", "Update user"),
        ("users:delete", "Delete user"),
        ("users:manage_roles", "Assign roles to users"),
        ("users:view_activity", "View user activity logs"),
    ],
    "posts": [
        ("posts:create", "Create blog post"),
        ("posts:read", "Read blog posts"),
        ("posts:update", "Update blog post"),
        ("posts:delete", "Delete blog post"),
        ("posts:publish", "Publish blog post"),
        ("posts:schedule", "Schedule blog post"),
        ("posts:bulk_update", "Bulk update posts"),
    ],
    "comments": [
        ("comments:create", "Create comment"),
        ("comments:read", "Read comments"),
        ("comments:update", "Update own comment"),
        ("comments:delete", "Delete comment"),
        ("comments:moderate", "Moderate comments"),
        ("comments:approve", "Approve comments"),
    ],
    "analytics": [
        ("analytics:view", "View analytics"),
        ("analytics:export", "Export analytics"),
    ],
    "settings": [
        ("settings:manage", "Manage system settings"),
        ("settings:manage_roles", "Manage roles and permissions"),
    ],
}


# Role to Permissions Mapping
ROLE_PERMISSIONS = {
    "super_admin": [
        # All permissions
        "users:list", "users:create", "users:read", "users:update", "users:delete",
        "users:manage_roles", "users:view_activity",
        "posts:create", "posts:read", "posts:update", "posts:delete", "posts:publish",
        "posts:schedule", "posts:bulk_update",
        "comments:create", "comments:read", "comments:update", "comments:delete",
        "comments:moderate", "comments:approve",
        "analytics:view", "analytics:export",
        "settings:manage", "settings:manage_roles",
    ],
    "admin": [
        # All except system settings
        "users:list", "users:create", "users:read", "users:update", "users:delete",
        "users:manage_roles", "users:view_activity",
        "posts:create", "posts:read", "posts:update", "posts:delete", "posts:publish",
        "posts:schedule", "posts:bulk_update",
        "comments:create", "comments:read", "comments:update", "comments:delete",
        "comments:moderate", "comments:approve",
        "analytics:view", "analytics:export",
        "settings:manage_roles",
    ],
    "editor": [
        # Content management
        "posts:create", "posts:read", "posts:update", "posts:delete", "posts:publish",
        "posts:schedule", "posts:bulk_update",
        "comments:read", "comments:moderate", "comments:approve",
        "users:read",
    ],
    "author": [
        # Own content only
        "posts:create", "posts:read", "posts:update",
        "comments:create", "comments:read",
    ],
    "user": [
        # Basic access
        "posts:read",
        "comments:create", "comments:read",
    ],
}


def seed_roles_and_permissions():
    """
    Seed the database with initial roles and permissions for the plugin.
    """
    db = SessionLocal()
    
    try:
        logger.info("🌱 Seeding user_management plugin roles and permissions...")
        
        # Create permissions
        permission_objects = {}
        for module, perms in PERMISSIONS.items():
            for perm_name, perm_desc in perms:
                existing = db.query(Permission).filter(
                    Permission.name == perm_name
                ).first()
                
                if not existing:
                    permission = Permission(
                        name=perm_name,
                        description=perm_desc,
                        module=module,
                    )
                    db.add(permission)
                    permission_objects[perm_name] = permission
                    logger.debug(f"  ➕ Permission: {perm_name}")
                else:
                    permission_objects[perm_name] = existing
        
        db.commit()
        logger.info(f"✅ Created/verified {len(permission_objects)} permissions")
        
        # Create roles
        role_objects = {}
        for role_config in SYSTEM_ROLES:
            existing = db.query(Role).filter(
                Role.name == role_config["name"]
            ).first()
            
            if not existing:
                role = Role(**role_config)
                
                # Assign permissions to role
                if role_config["name"] in ROLE_PERMISSIONS:
                    for perm_name in ROLE_PERMISSIONS[role_config["name"]]:
                        perm = db.query(Permission).filter(
                            Permission.name == perm_name
                        ).first()
                        if perm and perm not in role.permissions:
                            role.permissions.append(perm)
                
                db.add(role)
                role_objects[role_config["name"]] = role
                logger.debug(f"  ➕ Role: {role_config['name']}")
            else:
                role_objects[role_config["name"]] = existing
        
        db.commit()
        logger.info(f"✅ Created/verified {len(role_objects)} system roles")
        
        logger.info("🌱 User management seeding completed successfully!")
        logger.info("\n📋 System Roles:")
        for role_name in role_objects:
            role = role_objects[role_name]
            logger.info(f"   - {role_name} (level {role.level}): {len(role.permissions)} permissions")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ User management seeding failed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_roles_and_permissions()
