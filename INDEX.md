# User Management Plugin - Complete Index

## 📑 Quick Navigation

### 🚀 Getting Started
- **New to the plugin?** Start with [README_GITHUB.md](./README_GITHUB.md) for comprehensive overview
- **Want to contribute?** Read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines
- **Need to deploy?** Check [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **Understand structure?** See [REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md)

### 📦 Plugin Contents

#### Core Code
- **[__init__.py](./__init__.py)** - Plugin entry point and initialization
- **[models/user.py](./models/user.py)** - All 8 database models
- **[services/auth.py](./services/auth.py)** - Authentication service
- **[services/rbac.py](./services/rbac.py)** - RBAC service
- **[migrations/run_migrations.py](./migrations/run_migrations.py)** - Database setup
- **[migrations/seed_roles_and_permissions.py](./migrations/seed_roles_and_permissions.py)** - Initial data
- **[api/routes/](./api/routes/)** - API endpoint structure

#### Configuration
- **[requirements.txt](./requirements.txt)** - Python dependencies
- **[setup.py](./setup.py)** - pip installation config
- **[.env.example](./.env.example)** - Environment template
- **[Dockerfile](./Dockerfile)** - Docker image configuration
- **[docker-compose.yml](./docker-compose.yml)** - Development stack

#### Documentation
- **[README_GITHUB.md](./README_GITHUB.md)** - Complete project documentation (450+ lines)
- **[README.md](./README.md)** - Integrated plugin documentation
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contributing guidelines (300+ lines)
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Deployment guide
- **[REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md)** - Structure explanation
- **[LICENSE](./LICENSE)** - MIT License

---

## 🎯 Common Tasks

### Installation

**Option 1: From GitHub**
```bash
pip install git+https://github.com/GabForgeOnline/user-management-plugin.git
```

**Option 2: From Source**
```bash
git clone https://github.com/GabForgeOnline/user-management-plugin.git
cd user-management-plugin
pip install -e .
```

**Option 3: Docker**
```bash
docker-compose up -d
```

### Local Development

**Setup environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
docker-compose up -d postgres
python -m user_management.migrations.run_migrations
```

**Run tests:**
```bash
pytest tests/ -v --cov=user_management
```

**Code quality:**
```bash
black user_management/
flake8 user_management/
mypy user_management/
```

### Common Code Examples

**Create a user:**
```python
from user_management.services import AuthService
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://user:pass@localhost/gabforge")
session = Session(engine)

auth = AuthService(session)
user = auth.create_user("john_doe", "john@example.com", "password123")
```

**Check permissions:**
```python
from user_management.services import RBACService

rbac = RBACService(session)
if rbac.check_permission(user, "posts:create"):
    # User can create posts
```

**Assign roles:**
```python
rbac.assign_role(user, "editor")
```

---

## 📊 Database Schema

### Tables (10 total)

| Table | Purpose |
|-------|---------|
| users | User accounts and profiles |
| roles | Role definitions (5 system roles) |
| permissions | Permission definitions (50+) |
| user_roles | Many-to-many user-role mapping |
| role_permissions | Many-to-many role-permission mapping |
| user_sessions | JWT token tracking |
| user_activity_logs | Audit trail |
| user_preferences | Per-user settings |
| email_verification_tokens | Registration verification |
| password_reset_tokens | Password recovery |

### Models (8 total)

1. **User** - User accounts, authentication
2. **Role** - System roles with levels
3. **Permission** - Granular permissions
4. **UserRole** - User-role relationships
5. **RolePermission** - Role-permission relationships
6. **UserSession** - JWT token management
7. **UserActivityLog** - Activity tracking
8. **UserPreferences** - User settings

---

## 🔐 Security Features

### Authentication
- ✓ Secure password hashing (bcrypt, cost 12)
- ✓ JWT token-based authentication
- ✓ Token refresh mechanism
- ✓ Password recovery workflow
- ✓ Email verification

### Authorization
- ✓ Role-based access control (RBAC)
- ✓ 5 system roles with hierarchy
- ✓ 50+ granular permissions
- ✓ Dynamic permission checking
- ✓ Permission inheritance

### Audit & Compliance
- ✓ Complete activity logging
- ✓ IP address tracking
- ✓ User agent tracking
- ✓ Timestamp on all actions
- ✓ Session management

---

## 🏗️ System Roles & Permissions

### Roles (5)

| Role | Level | Access |
|------|-------|--------|
| Super Admin | 40 | Full system access |
| Admin | 30 | All except system settings |
| Editor | 20 | Content management |
| Author | 10 | Own content management |
| User | 0 | Basic read access |

### Permissions (50+)

#### Users Module
- `users:view` - View user list
- `users:view_profile` - View user profile
- `users:edit` - Edit user details
- `users:delete` - Delete users
- `users:manage_roles` - Assign/revoke roles

#### Posts Module
- `posts:create` - Create posts
- `posts:edit_own` - Edit own posts
- `posts:edit_others` - Edit any posts
- `posts:delete` - Delete posts
- `posts:publish` - Publish posts
- `posts:unpublish` - Unpublish posts
- `posts:schedule` - Schedule posts
- `posts:view_analytics` - View analytics

#### Comments Module
- `comments:create` - Create comments
- `comments:edit_own` - Edit own comments
- `comments:edit_others` - Edit any comments
- `comments:delete` - Delete comments
- `comments:moderate` - Moderate comments
- `comments:view` - View comments

#### Analytics Module
- `analytics:view_own` - View own analytics
- `analytics:view_all` - View all analytics
- `analytics:export` - Export data
- `analytics:view_system` - View system analytics

#### Settings Module
- `settings:view` - View settings
- `settings:edit` - Edit settings
- `settings:manage_plugins` - Manage plugins
- `settings:view_logs` - View logs

---

## 🔌 API Endpoints (30+)

### Authentication (6)
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### Users (6)
- `GET /api/users/me` - Get current user
- `GET /api/users/{id}` - Get user by ID
- `GET /api/users` - List users
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Deactivate user
- `GET /api/users/{id}/sessions` - Get user sessions

### Roles (6)
- `GET /api/roles` - List all roles
- `GET /api/roles/{id}` - Get role by ID
- `POST /api/users/{user_id}/roles/{role_id}` - Assign role
- `DELETE /api/users/{user_id}/roles/{role_id}` - Remove role
- `GET /api/users/{user_id}/roles` - Get user roles
- `POST /api/roles` - Create custom role

### Permissions (6)
- `GET /api/permissions` - List all permissions
- `GET /api/permissions/{id}` - Get permission by ID
- `GET /api/users/{user_id}/permissions` - Get user permissions
- `POST /api/permissions/check` - Check permission
- `GET /api/roles/{role_id}/permissions` - Get role permissions
- `POST /api/roles/{role_id}/permissions/{perm_id}` - Add permission to role

### Sessions (4)
- `GET /api/sessions` - List user sessions
- `GET /api/sessions/{session_id}` - Get session details
- `DELETE /api/sessions/{session_id}` - Logout session
- `DELETE /api/sessions` - Logout all sessions

### Preferences (2)
- `GET /api/preferences` - Get user preferences
- `PUT /api/preferences` - Update preferences

---

## 🧪 Testing

### Test Framework
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-asyncio** - Async testing

### Test Coverage
- Unit tests for models
- Unit tests for services
- Integration tests for API
- Database tests for migrations

### Running Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=user_management --cov-report=html

# Specific test
pytest tests/test_auth.py::test_authenticate_user -v
```

---

## 📚 Additional Resources

### External Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [passlib Documentation](https://passlib.readthedocs.io/)

### Community
- [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- [GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)
- Email: support@gabforge.local

---

## 🤝 Contributing

1. Read [CONTRIBUTING.md](./CONTRIBUTING.md)
2. Set up development environment
3. Create feature branch
4. Make changes and add tests
5. Submit pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## ✨ Features at a Glance

- ✅ User registration and authentication
- ✅ Secure password hashing (bcrypt)
- ✅ JWT token management
- ✅ Role-based access control
- ✅ 50+ granular permissions
- ✅ Activity logging
- ✅ Email verification
- ✅ Password reset
- ✅ Session management
- ✅ User preferences
- ✅ Docker containerization
- ✅ Complete documentation
- ✅ Open source (MIT)

---

## 📊 Version Info

- **Version**: 1.0.0
- **Status**: Production Ready
- **License**: MIT
- **Python**: 3.9+
- **Updated**: December 2024

---

## 🎯 Quick Links

| Item | Link |
|------|------|
| **Overview** | [README_GITHUB.md](./README_GITHUB.md) |
| **Contributing** | [CONTRIBUTING.md](./CONTRIBUTING.md) |
| **Deployment** | [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) |
| **Structure** | [REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md) |
| **License** | [LICENSE](./LICENSE) |
| **Config Template** | [.env.example](./.env.example) |
| **GitHub Issues** | [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues) |
| **Email Support** | support@gabforge.local |

---

**Last Updated**: December 2024  
**Maintained by**: GabForge Team  
**Repository**: https://github.com/GabForgeOnline/user-management-plugin
