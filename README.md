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


---

## ⚡ Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/fastapi-auth.git
cd fastapi-auth

2. Create and activate a virtual environment:

python -m venv env
# Windows
env\Scripts\activate
# Linux / Mac
source env/bin/activate

3. Install Dependencies 

pip install -r requirements.txt

4. run databsase migrations 

alembic upgrade head

## Enviroment variable 

JWT_SECRET_KEY=your_super_secret_key_1234567890abcdef
DATABASE_URL=sqlite+aiosqlite:///./app.db
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password

## Running the app

uvicorn main:app --reload


