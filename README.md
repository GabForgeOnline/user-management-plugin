# User Management Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791.svg)](https://www.postgresql.org/)

Comprehensive user management, authentication, and role-based access control (RBAC) plugin for GabForge.

## 🎯 Features

### Authentication & Security
- **Secure Password Hashing**: bcrypt with configurable cost factor
- **JWT Token Management**: Token-based authentication with refresh tokens
- **Password Recovery**: Secure password reset via email tokens
- **Email Verification**: Registration verification workflow
- **Session Management**: Track user sessions with IP and user agent

### Role-Based Access Control (RBAC)
- **5 System Roles**: Super Admin, Admin, Editor, Author, User
- **Hierarchical Permissions**: 50+ granular permissions across modules
- **Dynamic Role Assignment**: Assign/revoke roles at runtime
- **Permission Checking**: Built-in middleware for permission validation
- **Audit Trail**: Complete activity logging for compliance

### User Features
- **Profile Management**: Store user metadata and preferences
- **Activity Logging**: Track user actions across the system
- **Theme & Locale Preferences**: Per-user UI customization
- **Notification Settings**: Control notification preferences

## 📦 Installation

### Option 1: Direct Installation from Repository
```bash
pip install git+https://github.com/GabForgeOnline/user-management-plugin.git
```

### Option 2: From Source
```bash
git clone https://github.com/GabForgeOnline/user-management-plugin.git
cd user-management-plugin
pip install -e .
```

### Option 3: With Development Tools
```bash
pip install -e ".[dev]"
```

### Docker Installation
```bash
docker build -t user-management-plugin:latest .
docker run -e DATABASE_URL="postgresql://user:pass@localhost/gabforge" \
           -p 8000:8000 \
           user-management-plugin:latest
```

## 🚀 Quick Start

### 1. Initialize the Plugin

```python
from user_management import UserManagementPlugin

# Initialize plugin (creates tables, seeds roles/permissions)
plugin = UserManagementPlugin()
plugin.initialize()
```

### 2. Create a User

```python
from user_management.services import AuthService
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://user:pass@localhost/gabforge")
session = Session(engine)

auth_service = AuthService(session)
user = auth_service.create_user(
    username="john_doe",
    email="john@example.com",
    password="secure_password_123",
    first_name="John",
    last_name="Doe"
)
```

### 3. Authenticate User

```python
user = auth_service.authenticate_user("john_doe", "secure_password_123")
if user:
    print(f"Login successful: {user.username}")
else:
    print("Invalid credentials")
```

### 4. Check Permissions

```python
from user_management.services import RBACService

rbac_service = RBACService(session)

# Check single permission
if rbac_service.check_permission(user, "posts:create"):
    # Allow user to create posts
    print("User can create posts")

# Check multiple permissions
permissions = rbac_service.get_user_permissions(user)
print(f"User has {len(permissions)} permissions")

# Check role
if rbac_service.check_role(user, "editor"):
    print("User is an editor")
```

### 5. Assign Roles

```python
# Assign role to user
rbac_service.assign_role(user, "editor")

# Remove role from user
rbac_service.remove_role(user, "editor")
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    avatar_url VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    meta_data JSONB DEFAULT '{}'
);
```

### Roles Table
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    level INTEGER DEFAULT 0,
    is_system BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Permissions Table
```sql
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    module VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Other Tables
- **user_roles**: Many-to-many relationship between users and roles
- **role_permissions**: Many-to-many relationship between roles and permissions
- **user_sessions**: JWT token tracking for active sessions
- **user_activity_logs**: Audit trail of user actions
- **user_preferences**: Per-user settings and preferences
- **email_verification_tokens**: Tokens for email verification during registration
- **password_reset_tokens**: Tokens for password reset workflow

## 🔐 Security Features

### Password Security
- **bcrypt Hashing**: Industry-standard password hashing with configurable cost
- **No Plain-Text Storage**: Passwords never stored in plain text
- **Password Validation**: Enforce minimum strength requirements
- **Password History**: Optional prevention of password reuse

### Token Security
- **JWT Signed Tokens**: Cryptographically signed with secret key
- **Token Expiration**: Configurable token lifetime (default: 1 hour access, 7 days refresh)
- **Token Revocation**: Maintain session list for token validation
- **Secure Refresh**: Separate refresh tokens for extended access

### Session Management
- **IP Tracking**: Record user IP address for each session
- **User Agent Tracking**: Detect device/browser changes
- **Session Invalidation**: Force logout by session ID
- **Concurrent Session Control**: Limit sessions per user

### Audit Trail
- **Activity Logging**: Every user action logged with timestamp
- **IP & User Agent**: Session context for each action
- **Compliance Ready**: Complete audit trail for regulations

## 🎯 System Roles & Permissions

### 5 System Roles (by access level)

| Role | Level | Access |
|------|-------|--------|
| Super Admin | 40 | Full system access, user/role/permission management |
| Admin | 30 | All except system settings modification |
| Editor | 20 | Content management, publish/unpublish posts |
| Author | 10 | Create and manage own content |
| User | 0 | Basic access, read public content |

### Permission Modules

#### Users Module
- `users:view` - View user list
- `users:view_profile` - View user profile
- `users:edit` - Edit user details
- `users:delete` - Delete users
- `users:manage_roles` - Assign/revoke roles

#### Posts Module
- `posts:create` - Create new posts
- `posts:edit_own` - Edit own posts
- `posts:edit_others` - Edit any posts
- `posts:delete` - Delete posts
- `posts:publish` - Publish posts
- `posts:unpublish` - Unpublish posts
- `posts:schedule` - Schedule posts
- `posts:view_analytics` - View post analytics

#### Comments Module
- `comments:create` - Create comments
- `comments:edit_own` - Edit own comments
- `comments:edit_others` - Edit any comments
- `comments:delete` - Delete comments
- `comments:moderate` - Moderate comments
- `comments:view` - View comments

#### Analytics Module
- `analytics:view_own` - View own analytics
- `analytics:view_all` - View all user analytics
- `analytics:export` - Export analytics data
- `analytics:view_system` - View system-wide analytics

#### Settings Module
- `settings:view` - View system settings
- `settings:edit` - Edit system settings
- `settings:manage_plugins` - Enable/disable plugins
- `settings:view_logs` - View system logs

## 🔌 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password_123"
}
```

Response:
```json
{
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

#### Change Password
```http
POST /api/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "current_password": "old_password",
    "new_password": "new_password"
}
```

#### Forgot Password
```http
POST /api/auth/forgot-password
Content-Type: application/json

{
    "email": "john@example.com"
}
```

#### Reset Password
```http
POST /api/auth/reset-password
Content-Type: application/json

{
    "token": "reset_token_from_email",
    "new_password": "new_password"
}
```

### User Management Endpoints

#### Get Current User
```http
GET /api/users/me
Authorization: Bearer <access_token>
```

#### Get User by ID
```http
GET /api/users/{user_id}
Authorization: Bearer <access_token>
```

#### List Users
```http
GET /api/users?skip=0&limit=10&is_active=true
Authorization: Bearer <access_token>
```

#### Update User Profile
```http
PUT /api/users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Jane",
    "last_name": "Smith",
    "avatar_url": "https://...",
    "bio": "Software developer"
}
```

#### Deactivate User
```http
DELETE /api/users/{user_id}
Authorization: Bearer <access_token>
```

### Role Management Endpoints

#### Get User Roles
```http
GET /api/users/{user_id}/roles
Authorization: Bearer <access_token>
```

#### Assign Role
```http
POST /api/users/{user_id}/roles/{role_id}
Authorization: Bearer <access_token>
```

#### Remove Role
```http
DELETE /api/users/{user_id}/roles/{role_id}
Authorization: Bearer <access_token>
```

#### List Roles
```http
GET /api/roles
Authorization: Bearer <access_token>
```

### Permission Endpoints

#### Get User Permissions
```http
GET /api/users/{user_id}/permissions
Authorization: Bearer <access_token>
```

#### Check Permission
```http
POST /api/permissions/check
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "user_id": 1,
    "permission": "posts:create"
}
```

#### List All Permissions
```http
GET /api/permissions
Authorization: Bearer <access_token>
```

## 📋 Configuration

Create a `.env` file in your project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/gabforge

# JWT
JWT_SECRET_KEY=your_secret_key_here_min_32_characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1
JWT_REFRESH_EXPIRATION_DAYS=7

# Password Hashing
BCRYPT_COST=12

# Email (for password reset/verification)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=noreply@gabforge.com

# Application
APP_NAME=GabForge
APP_VERSION=1.0.0
DEBUG=False
```

## 🛠️ Development

### Install Development Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest tests/ -v --cov=user_management
```

### Code Quality
```bash
# Format code
black user_management/

# Lint code
flake8 user_management/

# Type checking
mypy user_management/
```

### Running Locally
```bash
# Using uvicorn directly
uvicorn user_management.main:app --reload --host 0.0.0.0 --port 8000

# Using Docker
docker-compose up -d
```

## 🔗 Integration with Other Plugins

This plugin provides the foundation for other GabForge plugins:

### Blog Plugin Dependencies
- Uses `User` model for post authors
- Uses RBAC for `posts:create`, `posts:edit`, `posts:publish` permissions
- Uses `UserActivityLog` for audit trail

### Comments Plugin Dependencies
- Uses `User` model for comment authors
- Uses RBAC for `comments:*` permissions
- Uses `UserSession` for user context

### Analytics Plugin Dependencies
- Uses `User` model for user identification
- Uses `UserActivityLog` for activity analysis
- Uses RBAC for `analytics:*` permissions

### Forum Plugin Dependencies
- Uses `User` model for forum members
- Uses RBAC for `forum:*` permissions
- Uses `UserPreferences` for notification settings

## 📚 Documentation

- [Database Schema Details](./docs/DATABASE_SCHEMA.md)
- [API Reference](./docs/API_REFERENCE.md)
- [Security Guidelines](./docs/SECURITY.md)
- [Contributing Guide](./CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)
- **Email**: support@gabforge.com

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT implementation
- [passlib](https://passlib.readthedocs.io/) - Password hashing

## 🗺️ Roadmap

- [ ] Email verification workflow
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 integration (Google, GitHub)
- [ ] LDAP/Active Directory support
- [ ] API key authentication for service-to-service calls
- [ ] Advanced analytics dashboard
- [ ] User import/export functionality
- [ ] Bulk role assignment
- [ ] Permission inheritance system

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintainer**: GabForge Team
