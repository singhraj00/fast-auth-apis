# FastAPI JWT Authentication API

A secure authentication API built with FastAPI featuring JWT access and refresh tokens, user registration, login, and protected routes.

## Features

- 🔐 User registration and login with email
- 🎫 JWT access and refresh token authentication
- 🔄 Automatic token refresh with secure httpOnly cookies
- 🔒 Password reset functionality
- 🛡️ Password hashing with bcrypt
- 🚪 Secure logout with token revocation
- 📱 RESTful API design
- 📋 Automatic API documentation with Swagger UI

## Tech Stack

- **FastAPI** - Modern Python web framework
- **JWT** - JSON Web Tokens for authentication
- **BCrypt** - Password hashing
- **SQLAlchemy** - Database ORM (optional)
- **Pydantic** - Data validation
- **Python 3.7+**

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd fastapi-jwt-auth
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
```

4. Create a `.env` file in the root directory:
```env
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Quick Start

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. Open your browser and visit:
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "msg": "user created"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** Refresh token is also set as an httpOnly secure cookie.

#### Refresh Token
```http
POST /auth/refresh
```

**Note:** Uses refresh token from httpOnly cookie automatically.

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** New refresh token is automatically set as httpOnly secure cookie.

### Protected Endpoints

#### Logout
```http
POST /auth/logout
```

**Note:** Uses refresh token from httpOnly cookie to revoke the session.

**Response:**
```json
{
  "msg": "logged out"
}
```

#### Forgot Password
```http
POST /auth/forgot-password
```

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "reset_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** In production, this token should be sent via email, not returned in response.

#### Change/Reset Password
```http
POST /auth/change-password
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "new_password": "newSecurePassword123"
}
```

**Response:**
```json
{
  "msg": "Password changed successfully"
}
```

## Authentication Flow

1. **Registration**: User creates account with username, email, and password
2. **Login**: User provides credentials and receives access + refresh tokens
3. **API Access**: Include access token in Authorization header for protected routes
4. **Token Refresh**: When access token expires, use refresh token to get new access token
5. **Logout**: Invalidate tokens (if using token blacklisting)

## Token Information

- **Access Token**: Short-lived (15 minutes by default), used for API requests
- **Refresh Token**: Long-lived (7 days by default), used to obtain new access tokens
- **Algorithm**: HS256 (HMAC with SHA-256)

## Usage Examples

### Python Requests
```python
import requests

# Register
response = requests.post("http://localhost:8000/auth/register", json={
    "email": "john@example.com",
    "password": "securepassword123"
})

# Login (refresh token set as httpOnly cookie automatically)
response = requests.post("http://localhost:8000/auth/login", json={
    "email": "john@example.com",
    "password": "securepassword123"
})
tokens = response.json()

# Access protected route
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
response = requests.get("http://localhost:8000/users/me", headers=headers)
user_data = response.json()

# Refresh token (uses httpOnly cookie automatically)
response = requests.post("http://localhost:8000/auth/refresh")
new_tokens = response.json()

# Forgot password
response = requests.post("http://localhost:8000/auth/forgot-password", json={
    "email": "john@example.com"
})
reset_data = response.json()

# Change password
response = requests.post("http://localhost:8000/auth/change-password", json={
    "token": reset_data["reset_token"],
    "new_password": "newSecurePassword123"
})
```

### JavaScript/Fetch
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'johndoe',
    password: 'securepassword123'
  })
});
const tokens = await loginResponse.json();

// Access protected route
const userResponse = await fetch('http://localhost:8000/users/me', {
  headers: { 'Authorization': `Bearer ${tokens.access_token}` }
});
const userData = await userResponse.json();
```

### cURL
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "john@example.com", "password": "securepassword123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepassword123"}'

# Access protected route
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer <your_access_token>"
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Token Refresh**: Secure token renewal without re-authentication
- **CORS Support**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request/response validation

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created (registration)
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid credentials/token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `500` - Internal Server Error

Example error response:
```json
{
  "detail": "Invalid credentials"
}
```

## Configuration

Environment variables (`.env` file):

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (if using)
DATABASE_URL=sqlite:///./app.db

# CORS (optional)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Project Structure

```
FASTAPI/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── script.py.mako         # Script template file
├── env.py                 # Environment configuration
├── alembic.ini            # Alembic migration configuration
├── schemas.py             # Pydantic schemas
├── crud.py                # Database CRUD operations
├── utils.py               # Utility functions
├── router.py              # Main router file
├── settings.py            # Application settings
├── models.py              # SQLAlchemy models
├── db.py                  # Database connection and session
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
├── app/
│   ├── __pycache__/       # Python cache
│   ├── versions/          # Alembic migration versions
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py      # Authentication endpoints
│   │   ├── utils.py       # JWT and password utilities
│   │   └── dependencies.py # Authentication dependencies
│   ├── models.py          # Database models (User, RefreshToken)
│   ├── db.py              # Database connection
│   └── settings.py        # Configuration settings
└── README.md
```

## Development

### Running Tests
```bash
pip install pytest httpx
pytest
```

### Code Formatting
```bash
pip install black isort
black .
isort .
```

### Type Checking
```bash
pip install mypy
mypy .
```

## Deployment

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use a strong `SECRET_KEY` (minimum 32 characters)
- Set appropriate token expiration times
- Implement rate limiting
- Use HTTPS in production
- Consider token blacklisting for logout
- Set up proper logging and monitoring
- Use environment variables for configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Review the API documentation at `/docs`
3. Create a new issue with detailed information

## Changelog

### v1.0.0
- Initial release
- User registration and login
- JWT access and refresh tokens
- Protected routes
- Basic user management

---

**Made with ❤️ using FastAPI**
