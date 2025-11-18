# Contributing to User Management Plugin

Thank you for your interest in contributing to the User Management Plugin! We appreciate your help in making this project better.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Git

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/your_username/user-management-plugin.git
   cd user-management-plugin
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

6. **Start PostgreSQL**
   ```bash
   docker-compose up -d postgres
   # Or use your local PostgreSQL installation
   ```

7. **Run database migrations**
   ```bash
   python -m user_management.migrations.run_migrations
   ```

## Development Workflow

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Write your code** following the style guide below
2. **Add tests** for new functionality
3. **Update documentation** if needed
4. **Run tests** to ensure everything works

### Code Style Guide

#### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

#### Example:
```python
def authenticate_user(
    username: str, password: str
) -> Optional[User]:
    """
    Authenticate a user with username and password.

    Args:
        username: The user's username
        password: The user's password

    Returns:
        User object if authentication successful, None otherwise

    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password are required")
    
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None
```

#### Naming Conventions
- Classes: PascalCase (e.g., `UserManagementPlugin`)
- Functions: snake_case (e.g., `authenticate_user`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_PASSWORD_LENGTH`)
- Private functions: _snake_case (e.g., `_hash_password`)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=user_management --cov-report=html

# Run specific test
pytest tests/test_auth.py::test_authenticate_user -v
```

### Code Quality Tools

```bash
# Format code with black
black user_management/

# Lint with flake8
flake8 user_management/

# Type checking with mypy
mypy user_management/

# Run all checks
black user_management/ && flake8 user_management/ && mypy user_management/
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature/fix changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build, dependency, or tool changes

### Examples
```bash
git commit -m "feat(auth): add password strength validation"
git commit -m "fix(rbac): correct permission inheritance in role hierarchy"
git commit -m "docs(readme): add API endpoint examples"
git commit -m "test(auth): add password hashing tests"
```

## Pull Request Process

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill in the PR description following the template
   - Link related issues using "Fixes #123"

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix (non-breaking change fixing an issue)
   - [ ] New feature (non-breaking change adding functionality)
   - [ ] Breaking change (fix or feature causing existing functionality to change)

   ## How Has This Been Tested?
   Describe the test plan

   ## Checklist
   - [ ] My code follows the code style of this project
   - [ ] I have updated the documentation
   - [ ] I have added tests for my changes
   - [ ] All new and existing tests pass
   - [ ] My commit messages follow the guidelines
   ```

4. **Address Review Comments**
   - Make requested changes
   - Commit with descriptive messages
   - Push to your branch
   - Don't force push unless asked

5. **Merge**
   - Maintainers will merge when approved
   - Delete your feature branch after merge

## Testing Guidelines

### Writing Tests

```python
# test_auth.py
import pytest
from user_management.services import AuthService
from user_management.models import User

class TestAuthService:
    """Tests for AuthService."""

    def test_hash_password_creates_different_hash(self):
        """Test that hashing same password creates different hashes."""
        password = "test_password_123"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)
        assert hash1 != hash2

    def test_verify_password_success(self):
        """Test password verification with correct password."""
        password = "test_password_123"
        hash_value = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hash_value) is True

    def test_verify_password_failure(self):
        """Test password verification with incorrect password."""
        password = "test_password_123"
        hash_value = AuthService.hash_password(password)
        assert AuthService.verify_password("wrong_password", hash_value) is False
```

### Test Coverage Requirements
- Minimum 80% code coverage
- All public methods must have tests
- Test both success and failure cases
- Use descriptive test names

## Documentation Guidelines

### Docstring Format

```python
def create_user(
    username: str,
    email: str,
    password: str,
    first_name: Optional[str] = None
) -> User:
    """
    Create a new user account.

    This function creates a new user with the provided credentials
    and optional profile information.

    Args:
        username: The desired username (3-255 characters, alphanumeric)
        email: The user's email address (valid format required)
        password: The password (minimum 8 characters)
        first_name: Optional first name of the user

    Returns:
        User: The created user object with ID

    Raises:
        ValueError: If username/email already exists or invalid format
        SecurityError: If password doesn't meet security requirements

    Example:
        >>> user = create_user(
        ...     username="john_doe",
        ...     email="john@example.com",
        ...     password="SecurePassword123!"
        ... )
        >>> print(user.id)
        1
    """
```

## Reporting Issues

### Security Vulnerabilities
**Do not create a public GitHub issue for security vulnerabilities.**
Email security@gabforge.local with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Bug Reports
Include:
- Python and FastAPI versions
- PostgreSQL version
- Detailed description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces
- Code examples

### Feature Requests
Include:
- Clear description of the feature
- Use case and motivation
- Examples of how it would work
- Alternative approaches (if any)

## Project Structure

```
user-management-plugin/
├── user_management/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── rbac.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── roles.py
│   │       └── permissions.py
│   └── migrations/
│       ├── __init__.py
│       ├── run_migrations.py
│       └── seed_roles_and_permissions.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_rbac.py
│   └── test_models.py
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── .env.example
```

## Helpful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## Community

- **Discussions**: [GitHub Discussions](https://github.com/GabForgeOnline/user-management-plugin/discussions)
- **Issues**: [GitHub Issues](https://github.com/GabForgeOnline/user-management-plugin/issues)
- **Email**: support@gabforge.local

## Recognition

Contributors will be recognized in:
- The README.md file
- Release notes
- GitHub contributors page

Thank you for contributing to User Management Plugin! 🎉
