from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from ..db import AsyncSessionLocal
from ..models import User, RefreshToken
from .utils import verify_password, hash_password, create_access_token, create_refresh_token, create_reset_token, verify_reset_token
from ..settings import settings
import hashlib
from datetime import datetime,timezone
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.models import User
import uuid

router = APIRouter(prefix="/auth")

@router.post("/register", status_code=201)
async def register(data: dict):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.email==data["email"]))
        if q.scalar_one_or_none():
            raise HTTPException(400, "Email exists")
        user = User(email=data["email"], hashed_password=hash_password(data["password"]))
        session.add(user)
        await session.commit()
        return {"msg":"user created"}

@router.post("/login")
async def login(request: Request, response: Response, payload: dict):
    # payload: {"email":.., "password":..}
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.email==payload["email"]))
        user = q.scalar_one_or_none()
        if not user or not verify_password(payload["password"], user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        access_token = create_access_token(str(user.id))
        refresh_plain, refresh_hash, expires_at = create_refresh_token()
        rt = RefreshToken(user_id=user.id, token=refresh_hash, ip=request.client.host, expires_at=expires_at)
        session.add(rt)
        await session.commit()

        # set secure httpOnly cookie for refresh token
        response = JSONResponse({"access_token": access_token, "refresh_token":refresh_hash, "token_type": "bearer"})
        response.set_cookie(
            key="refresh_token",
            value=refresh_plain,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*settings.REFRESH_TOKEN_EXPIRE_DAYS,
            path=settings.REFRESH_TOKEN_PATH
        )
        return response

@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh = request.cookies.get("refresh_token")
    if not refresh:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing refresh token")
    refresh_hash = hashlib.sha256(refresh.encode()).hexdigest()
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(RefreshToken).where(RefreshToken.token==refresh_hash))
        db_rt = q.scalar_one_or_none()
        if not db_rt or db_rt.revoked or db_rt.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
        # rotate: revoke old, create new
        db_rt.revoked = True
        session.add(db_rt)
        new_plain, new_hash, new_expires = create_refresh_token()
        new_rt = RefreshToken(user_id=db_rt.user_id, token=new_hash, expires_at=new_expires)
        session.add(new_rt)
        await session.commit()
        new_access = create_access_token(str(db_rt.user_id))
        response = JSONResponse({"access_token": new_access, "token_type": "bearer"})
        response.set_cookie("refresh_token", new_plain, httponly=True, secure=True, samesite="lax",
                            max_age=60*60*24*settings.REFRESH_TOKEN_EXPIRE_DAYS, path=settings.REFRESH_TOKEN_PATH)
        return response

@router.post("/logout")
async def logout(request: Request, response: Response):
    refresh = request.cookies.get("refresh_token")
    if refresh:
        refresh_hash = hashlib.sha256(refresh.encode()).hexdigest()
        async with AsyncSessionLocal() as session:
            q = await session.execute(select(RefreshToken).where(RefreshToken.token_hash==refresh_hash))
            db_rt = q.scalar_one_or_none()
            if db_rt:
                db_rt.revoked = True
                session.add(db_rt)
                await session.commit()
    # clear cookie
    response = JSONResponse({"msg":"logged out"})
    response.delete_cookie("refresh_token", path=settings.REFRESH_TOKEN_PATH)
    return response





# ----------- Schemas -----------
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# ----------- DB Dependency -----------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ----------- Forgot Password API -----------
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # generate reset token (JWT)
    token = create_reset_token({"sub": str(user.id)})

    # ⚠️ For now just return it (in production, send via email)
    return {"reset_token": token}


# ----------- Change Password API -----------
@router.post("/change-password")
async def change_password(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    payload = verify_reset_token(data.token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # update password
    user.hashed_password = hash_password(data.new_password)
    await db.commit()

    return {"msg": "Password changed successfully"}