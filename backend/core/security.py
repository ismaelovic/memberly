from datetime import datetime, timedelta
from typing import Optional, List
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.config import settings

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
    data: dict, roles: List[str], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "roles": roles})
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
import aioredis

redis = aioredis.from_url(settings.redis_url)


async def revoke_token(token: str):
    await redis.set(
        f"revoked:{token}", "true", ex=settings.access_token_expire_minutes * 60
    )


async def is_token_revoked(token: str) -> bool:
    return await redis.exists(f"revoked:{token}") > 0


# Token renewal


def renew_access_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    if payload:
        roles = payload.get("roles", [])
        return create_access_token(data=payload, roles=roles)
    return None
