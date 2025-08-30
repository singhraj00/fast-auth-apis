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
