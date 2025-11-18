#!/usr/bin/env python
"""
Setup script for User Management Plugin
Enables: pip install git+https://github.com/GabForgeOnline/user-management-plugin.git
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="user-management-plugin",
    version="1.0.0",
    author="GabForge Team",
    author_email="team@gabforge.local",
    description="User Management plugin for GabForge - RBAC, authentication, and user lifecycle management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GabForgeOnline/user-management-plugin",
    project_urls={
        "Bug Tracker": "https://github.com/GabForgeOnline/user-management-plugin/issues",
        "Documentation": "https://github.com/GabForgeOnline/user-management-plugin/wiki",
        "Source Code": "https://github.com/GabForgeOnline/user-management-plugin",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-dotenv>=1.0.0",
        "PyJWT>=2.10.0",
        "passlib[bcrypt]>=1.7.4",
        "email-validator>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "docs": [
            "sphinx>=7.0",
            "sphinx-rtd-theme>=1.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "user-management-cli=user_management.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "user-management",
        "rbac",
        "authentication",
        "authorization",
        "permissions",
        "roles",
        "gabforge",
        "plugin",
    ],
)
