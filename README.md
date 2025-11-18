# User Management Plugin

**Version:** 1.0.0  
**Status:** Phase 2.1 - Development  
**Author:** GabForge Team

---

## 📋 Overview

User Management Plugin is a standalone, reusable authentication and RBAC (Role-Based Access Control) system that can be used across multiple platforms and applications.

This plugin provides:
- **User Registration & Authentication** - Email/password registration with email verification
- **Token Management** - JWT tokens with refresh token support
- **Role-Based Access Control** - Hierarchical role system (super_admin, admin, editor, author, user)
- **Permission Management** - Fine-grained permissions (format: "module:action")
- **Activity Logging** - Audit trail of user actions for security and compliance
- **User Profiles** - Extended user profiles with preferences
- **Password Management** - Secure password hashing (bcrypt), password reset

---

## 🏗️ Plugin Structure

```
user_management/
├── __init__.py                 # Plugin entry point
├── models/
│   ├── __init__.py
│   └── user.py                # All models (User, Role, Permission, etc.)
├── services/
│   ├── __init__.py
│   ├── auth.py                # Authentication service
│   └── rbac.py                # RBAC service
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py            # Auth endpoints (register, login, etc.)
│       ├── users.py           # User profile endpoints
│       └── admin.py           # Admin management endpoints
├── migrations/
│   ├── __init__.py
│   ├── run_migrations.py      # Create tables
│   └── seed_roles_and_permissions.py  # Seed initial data
├── README.md
└── requirements.txt
```

---

## 🗄️ Database Schema

### Core Tables

#### `users`
- `id` (PK) - User ID
- `username` - Unique username
- `email` - Unique email
- `password_hash` - Bcrypt hashed password
- `first_name`, `last_name` - User name
- `avatar_url` - Profile picture
- `bio` - User biography
- `phone` - Phone number
- `is_active` - Account status
- `is_email_verified` - Email verification status
- `email_verified_at` - When email was verified
- `last_login` - Last login timestamp
- `created_at`, `updated_at`, `deleted_at` - Timestamps (soft delete support)

#### `roles`
- `id` (PK) - Role ID
- `name` - Unique role name (admin, editor, author, user)
- `description` - Role description
- `level` - Hierarchy level (0-40)
- `is_system` - Cannot delete system roles
- `created_at` - Creation timestamp

#### `permissions`
- `id` (PK) - Permission ID
- `name` - Unique permission name (format: "module:action")
- `description` - Permission description
- `module` - Permission module (posts, comments, users, etc.)
- `created_at` - Creation timestamp

#### `user_roles` (Junction Table)
- `user_id` (FK) - Reference to users
- `role_id` (FK) - Reference to roles
- `assigned_at` - When role was assigned
- `assigned_by` (FK) - Admin who assigned role
- `expires_at` - Optional role expiry date

#### `role_permissions` (Junction Table)
- `role_id` (FK) - Reference to roles
- `permission_id` (FK) - Reference to permissions

### Supporting Tables

#### `user_sessions`
- Track active user sessions for token management
- Stores JWT tokens with expiry
- IP address and user agent tracking

#### `user_activity_logs`
- Audit trail of all user actions
- Tracks: login, logout, post creation, comments, etc.
- Stores IP, user agent, metadata

#### `user_preferences`
- User settings: theme, language, timezone
- Email notification preferences
- Two-factor authentication status

#### `email_verification_tokens`
- Tokens for email verification during registration
- Auto-expire after 24 hours

#### `password_reset_tokens`
- Tokens for password reset
- Auto-expire after 1 hour

---

## 🔐 Security Features

✅ **Password Security**
- Bcrypt hashing with salt
- Never stores plaintext passwords
- Configurable hash rounds

✅ **Token Security**
- JWT tokens with configurable expiry
- Refresh token mechanism
- Token rotation on refresh
- Session tracking

✅ **Input Validation**
- Email format validation
- Password strength requirements (min 8 chars)
- Username validation (alphanumeric + underscore)
- SQL injection prevention (ORM)

✅ **Email Verification**
- Confirmation token required
- Token expires after 24 hours
- Resend verification email support

✅ **Password Reset**
- Reset token required
- Token expires after 1 hour
- New password hashed before storage

✅ **Rate Limiting** (Recommended)
- Limit login attempts (5 per 15 min)
- Limit registration (1 per IP per hour)
- Limit password reset (3 per email per hour)

✅ **Activity Logging**
- All user actions logged
- Security events tracked
- IP and user agent stored
- Audit trail for compliance

---

## 👥 Role Hierarchy

### System Roles

| Role | Level | Description | Use Case |
|------|-------|-------------|----------|
| super_admin | 40 | Full system access | System administrator |
| admin | 30 | Full access (except system settings) | Content admin |
| editor | 20 | Manage all content, moderate | Content moderator |
| author | 10 | Create and edit own content | Content creator |
| user | 0 | Basic access (read, comment) | End user |

### Default Permissions by Role

**Super Admin:** All permissions  
**Admin:** All except `settings:manage`  
**Editor:** Content management + user read  
**Author:** Own content only  
**User:** Read posts + create comments  

---

## 📦 Installation

### 1. Add to Requirements
```bash
# Already in main requirements.txt:
# - passlib[bcrypt]
# - PyJWT
# - SQLAlchemy
```

### 2. Initialize Plugin
```python
# In main.py
from plugins.user_management import UserManagementPlugin

plugin = UserManagementPlugin()
plugin.initialize()  # Creates tables and seeds data
```

### 3. Register Models
```python
# Models are automatically registered via plugin_manager
from plugins.user_management.models import User, Role, Permission
```

---

## 🚀 Usage Examples

### User Registration
```python
from plugins.user_management.services.auth import AuthService

new_user = AuthService.create_user(
    db=db_session,
    email="user@example.com",
    username="john_doe",
    password="securepassword123",
    first_name="John",
    last_name="Doe"
)
```

### User Authentication
```python
user = AuthService.authenticate_user(
    db=db_session,
    email="user@example.com",
    password="securepassword123"
)

if user:
    print(f"✅ User authenticated: {user.email}")
```

### Check Permission
```python
from plugins.user_management.services.rbac import RBACService

if RBACService.check_permission(user, "posts:create"):
    # Allow user to create post
    pass
```

### Assign Role
```python
RBACService.assign_role(db_session, user, "editor")
```

### Get User Permissions
```python
permissions = RBACService.get_user_permissions(user)
# Returns: {'posts:create', 'posts:read', ...}
```

---

## 🔌 Integration Points

### With Blog Plugin (Phase 2.2)
```python
# Check author can create posts
if RBACService.check_permission(user, "posts:create"):
    create_blog_post(user, content)

# Track in activity log
log_activity(user, "post_created", entity_type="post", entity_id=post.id)
```

### With Comments Plugin (Phase 2.3)
```python
# Check user can comment
if RBACService.check_permission(user, "comments:create"):
    create_comment(user, post_id, content)

# Editor can moderate comments
if RBACService.check_permission(user, "comments:moderate"):
    approve_comment(comment_id)
```

### With Analytics Plugin (Phase 2.4)
```python
# Track per-user analytics
log_activity(user, "view", entity_type="post", entity_id=post.id)

# Get user's activity
activities = user.activity_logs
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/test_auth_service.py
pytest tests/test_rbac_service.py
pytest tests/test_models.py
```

### Integration Tests
```bash
pytest tests/test_user_registration_flow.py
pytest tests/test_authentication_flow.py
```

### API Tests
```bash
pytest tests/api/test_auth_endpoints.py
pytest tests/api/test_user_endpoints.py
```

---

## 📚 API Endpoints (Phase 2 - To be implemented)

### Authentication
```
POST   /api/auth/register           - Register new user
POST   /api/auth/verify-email       - Verify email
POST   /api/auth/login              - Login
POST   /api/auth/logout             - Logout
POST   /api/auth/refresh-token      - Refresh JWT
POST   /api/auth/forgot-password    - Request password reset
POST   /api/auth/reset-password     - Reset password
```

### User Profile
```
GET    /api/users/me                - Get current user
PUT    /api/users/me                - Update profile
GET    /api/users/:id               - Get user public profile
PUT    /api/users/me/preferences    - Update preferences
```

### Admin
```
GET    /api/admin/users             - List users
GET    /api/admin/users/:id         - User details
PUT    /api/admin/users/:id         - Update user (admin)
POST   /api/admin/users/:id/roles   - Assign role
GET    /api/admin/roles             - List roles
GET    /api/admin/permissions       - List permissions
```

---

## 🔄 Migration Path to Separate Repository

This plugin is designed to be moved to a separate GitHub repository:

```
GabForgeOnline/user-management-plugin
├── README.md
├── setup.py
├── requirements.txt
├── user_management/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   ├── api/
│   └── migrations/
└── tests/
```

**Steps to separate:**
1. Create new GitHub repo: `GabForgeOnline/user-management-plugin`
2. Move plugin code to new repo
3. Create `setup.py` for pip installation
4. Reference from main site via pip: `pip install git+https://github.com/GabForgeOnline/user-management-plugin.git`

---

## 🔧 Configuration

### Environment Variables
```
# Optional - default values provided
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
JWT_REFRESH_EXPIRATION_DAYS=7

PASSWORD_HASH_ROUNDS=12
PASSWORD_MIN_LENGTH=8

EMAIL_VERIFICATION_EXPIRY_HOURS=24
PASSWORD_RESET_EXPIRY_HOURS=1
```

---

## 📝 Changelog

### v1.0.0 (2025-11-19)
- Initial release
- User registration and authentication
- RBAC system with hierarchical roles
- Activity logging and audit trail
- User profiles and preferences
- Password management
- Email verification

---

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: [user-management-plugin/issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- Email: team@gabforge.com

---

## 📄 License

MIT License - See LICENSE file

---

**Plugin Status:** ✅ Ready for Phase 2.1 Implementation  
**Last Updated:** 2025-11-19
