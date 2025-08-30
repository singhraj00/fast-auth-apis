# FastAPI Authentication System 🚀

A simple and modern **FastAPI** project that handles user authentication with JWT tokens, including password reset functionality.

---

## 🌟 Features

- ✅ User Registration & Login  
- ✅ JWT-based Access & Refresh Tokens  
- ✅ Forgot Password & Change Password  
- ✅ Secure Password Hashing (bcrypt)  
- ✅ Async Database Access (SQLAlchemy)  
- ✅ Easy to extend & maintain  

---

## 📂 Project Structure

```text
fastapi-auth/
├── app/
│   ├── auth/
│   │   ├── router.py        # Auth routes
│   │   ├── models.py        # User & token models
│   │   └── utils.py         # Helpers like email sender
│   ├── db.py                # DB session setup
│   └── security.py          # Password & JWT utilities
├── migrations/              # Alembic migrations
│   └── versions/            # Auto-generated migration files
├── env/                     # Virtual environment
├── .env                     # Environment variables (ignored)
├── main.py                  # FastAPI app entry point
├── requirements.txt
└── README.md
```

## ⚡ Installation & Setup (All-in-One Terminal)

``` text 

# 1. Clone the repository
git clone https://github.com/yourusername/fastapi-auth.git
cd fastapi-auth

# 2. Create and activate virtual environment
python -m venv env
# Windows
env\Scripts\activate
# Linux / Mac
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
alembic upgrade head

# 5. Create .env file with environment variables
echo "JWT_SECRET_KEY=your_super_secret_key_1234567890abcdef" >> .env
echo "DATABASE_URL=sqlite+aiosqlite:///./app.db" >> .env
echo "EMAIL_USER=your_email@example.com" >> .env
echo "EMAIL_PASS=your_email_password" >> .env

# 6. Run the FastAPI app
uvicorn main:app --reload

```

| Endpoint           | Method | Description                         |
| ------------------ | ------ | ----------------------------------- |
| `/register`        | POST   | Register a new user                 |
| `/login`           | POST   | Login and get JWT tokens            |
| `/refresh`         | POST   | Refresh access token                |
| `/forgot-password` | POST   | Send password reset token via email |
| `/change-password` | POST   | Change password using reset token   |

## 📝 Example Usage

### Register a new user:

POST /register
{
  "email": "user@example.com",
  "password": "MySecret123"
}

Request password reset token:

POST /forgot-password
{
  "email": "user@example.com"
}


Change password:

POST /change-password
{
  "token": "your_reset_token_here",
  "new_password": "NewStrongPass123"
}


