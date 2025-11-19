# User Management Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791.svg)](https://www.postgresql.org/)

**A completely independent, portable user management and authentication plugin** that works with ANY website, framework, or platform. Not tied to GabForge CMS.

## 🎯 What Makes This Special

✅ **Truly Independent** - Zero dependencies on GabForge or any host application  
✅ **Portable** - Works standalone or integrated into any project  
✅ **Framework Agnostic** - Use with FastAPI, Flask, Django, or any ASGI/WSGI app  
✅ **Database Flexible** - PostgreSQL, MySQL, or SQLite  
✅ **Production Ready** - Fully tested, documented, and deployable  
✅ **Easy Integration** - Simple REST API with JWT authentication

## ✨ Features

- **JWT Authentication** - Secure token-based auth with refresh tokens
- **User Registration & Login** - Complete auth flow with password validation
- **Role-Based Access Control (RBAC)** - 5 system roles with 50+ granular permissions
- **Password Security** - bcrypt hashing with configurable security levels
- **Session Management** - Track user sessions with IP/device detection
- **Activity Logging** - Audit trail for compliance and security monitoring
- **User Preferences** - Customizable per-user settings
- **Email Workflows** - Password reset and email verification ready to integrate
- **Docker Ready** - Production-grade containerization included

## 🚀 Quick Start (5 minutes)

### 1. Install
```bash
# Clone repository
git clone https://github.com/GabForgeOnline/user-management-plugin.git
cd user-management-plugin/production

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure
Create `.env`:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/user_management
JWT_SECRET_KEY=your-secret-key-min-32-chars-change-in-production
DEBUG=false
```

### 3. Initialize Database
```bash
python -c "from user_management.config import init_db; init_db()"
python -m user_management.migrations.seed_roles_and_permissions
```

### 4. Run
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

🎉 API running at `http://localhost:8000/api/docs`

## 📚 API Documentation

### Authentication Endpoints

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

#### Refresh Token
```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### Change Password
```bash
POST /api/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "OldPassword123!",
  "new_password": "NewPassword456!"
}
```

### Full API Docs
Visit `http://localhost:8000/api/docs` for interactive Swagger documentation

## 🔌 Integration Examples

### With FastAPI
```python
from fastapi import FastAPI, Depends
from user_management.app import create_app
from user_management.config import get_db
from user_management.services.auth import AuthService

# Option 1: Run as standalone service
app = create_app()

# Option 2: Integrate routes into existing app
main_app = FastAPI()
user_app = create_app()

# Include user management routes
for route in user_app.routes:
    main_app.routes.append(route)
```

### With Flask
```python
# Use the REST API endpoints via HTTP requests
import requests

# Register
response = requests.post("http://localhost:8000/api/auth/register", json={
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!"
})
user = response.json()

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "email": "user@example.com",
    "password": "SecurePassword123!"
})
tokens = response.json()
```

### With Django
```python
# Use the REST API as a microservice
# Call endpoints from Django views

from django.http import JsonResponse
import requests

def login_user(request):
    response = requests.post("http://user-mgmt:8000/api/auth/login", json={
        "email": request.POST.get("email"),
        "password": request.POST.get("password")
    })
    return JsonResponse(response.json())
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t user-management-plugin:latest .
```

### Run Container
```bash
docker run \
  -e DATABASE_URL=postgresql://user:password@db:5432/user_management \
  -e JWT_SECRET_KEY=your-secret-key \
  -p 8000:8000 \
  user-management-plugin:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: user_management
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

  user-management:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/user_management
      JWT_SECRET_KEY: your-secret-key
    depends_on:
      - db
```

## 🔐 Security

- **Password Hashing**: bcrypt with 12 rounds (configurable)
- **JWT Tokens**: Cryptographically signed, expiring tokens
- **Token Refresh**: Secure refresh token rotation mechanism
- **Session Tracking**: IP address and user agent logging
- **HTTPS Ready**: Works with SSL/TLS proxies
- **CORS Configurable**: Control access from frontend apps

## ⚙️ Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgresql://... | Database connection string |
| `JWT_SECRET_KEY` | (required) | Secret key for signing tokens (min 32 chars) |
| `JWT_ALGORITHM` | HS256 | JWT signing algorithm |
| `JWT_EXPIRATION_HOURS` | 24 | Access token expiration |
| `JWT_REFRESH_EXPIRATION_DAYS` | 7 | Refresh token expiration |
| `BCRYPT_COST` | 12 | Password hashing cost (10-12) |
| `SMTP_HOST` | smtp.gmail.com | Email server hostname |
| `SMTP_PORT` | 587 | Email server port |
| `SMTP_USER` | | Email account username |
| `SMTP_PASSWORD` | | Email account password |
| `SENDER_EMAIL` | noreply@example.com | Email sender address |
| `DEBUG` | false | Enable debug mode |

## 📚 Full Documentation

- **[Installation Guide](./INSTALLATION.md)** - Detailed setup instructions
- **[Configuration Guide](./CONFIGURATION.md)** - All configuration options
- **[API Reference](./API.md)** - Complete endpoint documentation
- **[Integration Guide](./INTEGRATION.md)** - Framework integration examples
- **[Contributing](./CONTRIBUTING.md)** - Contributing guidelines

## 🛠 Development

### Setup Development Environment
```bash
git clone https://github.com/GabForgeOnline/user-management-plugin.git
cd user-management-plugin/production

# Install with dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/ --cov=user_management

# Format code
black user_management/
```

### Run Locally
```bash
uvicorn app:app --reload
```

## 📝 License

MIT License - See [LICENSE](./LICENSE) file for details

## 💬 Support

- **Bug Reports**: [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- **Questions**: [GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)
- **Documentation**: [Docs](./docs)

## 🙏 Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Token implementation
- [passlib](https://passlib.readthedocs.io/) - Password hashing library

---

**Standalone** • **Portable** • **Production-Ready** • **Framework-Agnostic**

Version 1.0.0 | MIT License
