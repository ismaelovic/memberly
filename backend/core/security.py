from datetime import datetime, timedelta
from typing import Optional, List
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings
import asyncio
from redis.asyncio import Redis

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"

# Password hashing


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT token creation


def create_access_token(
    data: dict, role: str, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "role": str(role)})  # Ensure role is a string
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.refresh_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


# JWT token validation


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Token revocation (using Redis as an example)
redis = Redis.from_url(settings.redis_url)


async def revoke_token(token: str):
    try:
        await redis.set(
            f"revoked:{token}", "true", ex=settings.access_token_expire_minutes * 60
        )
    except asyncio.TimeoutError:
        # Handle timeout error
        pass


async def is_token_revoked(token: str) -> bool:
    try:
        return await redis.exists(f"revoked:{token}") > 0
    except asyncio.TimeoutError:
        # Handle timeout error
        return False


# Token renewal


def renew_access_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    if payload:
        role = payload.get("role", "")
        return create_access_token(data=payload, role=role)
    return None
