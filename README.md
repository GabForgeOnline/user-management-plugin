# User Management Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791.svg)](https://www.postgresql.org/)

A production-ready user management and authentication plugin for GabForge, featuring secure authentication, role-based access control (RBAC), and comprehensive audit logging.

## ✨ Features

- **Authentication**: Secure JWT-based authentication with refresh tokens
- **Password Security**: bcrypt hashing with configurable cost factors
- **Role-Based Access Control**: 5 system roles with 50+ granular permissions
- **Session Management**: Track and manage user sessions with IP/device detection
- **Activity Logging**: Complete audit trail for compliance and security
- **Email Workflows**: Email verification and password reset functionality
- **User Preferences**: Per-user settings for theme, locale, and notifications
- **Docker Ready**: Production-grade Dockerfile with health checks

## 📦 Installation

### From PyPI (when published)
```bash
pip install user-management-plugin
```

### From GitHub
```bash
pip install git+https://github.com/GabForgeOnline/user-management-plugin.git
```

### From Source
```bash
git clone https://github.com/GabForgeOnline/user-management-plugin.git
cd user-management-plugin
pip install -e .
```

### Docker
```bash
docker build -t user-management-plugin:latest .
docker-compose up
```

## 🚀 Quick Start

### Basic Usage
```python
from user_management import UserManagementPlugin

# Initialize plugin
plugin = UserManagementPlugin()
plugin.initialize()
```

### Authentication
```python
from user_management.services import AuthService

auth = AuthService(db_session)

# Register user
user = auth.create_user(
    username="john_doe",
    email="john@example.com",
    password="secure_password"
)

# Login
user = auth.authenticate_user("john_doe", "secure_password")
```

### Access Control
```python
from user_management.services import RBACService

rbac = RBACService(db_session)

# Check permission
if rbac.check_permission(user, "posts:create"):
    # User can create posts
    pass

# Assign role
rbac.assign_role(user, "editor")
```

## 📚 Documentation

- **[Full Documentation](./CONTRIBUTING.md)** - Contributing guide with detailed API documentation
- **[GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)** - Report bugs or request features
- **[GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)** - Community discussions

## ⚙️ Configuration

### Environment Variables
Create a `.env` file (see `.env.example`):

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/gabforge
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1
JWT_REFRESH_EXPIRATION_DAYS=7
BCRYPT_COST=12
```

### Database Setup
The plugin automatically creates all required tables on initialization. Supported databases:
- PostgreSQL 12+
- SQLite 3.24+ (for development)

## 🔐 Security

- **Password Hashing**: Industry-standard bcrypt with configurable cost
- **Token Security**: JWT signed tokens with expiration
- **Session Tracking**: IP and user agent logging for anomaly detection
- **Audit Trail**: Complete activity logging for compliance

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 💬 Support

- **Email**: gabforge.online@gmail.com
- **Issues**: [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [passlib](https://passlib.readthedocs.io/)

---

**Status**: Production Ready | **Version**: 1.0.0 | **License**: MIT
