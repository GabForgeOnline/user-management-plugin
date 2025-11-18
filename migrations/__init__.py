"""
migrations/__init__.py - Plugin migrations
"""

from .run_migrations import run_migrations
from .seed_roles_and_permissions import seed_roles_and_permissions

__all__ = ["run_migrations", "seed_roles_and_permissions"]
