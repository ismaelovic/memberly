import aioredis
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        try:
            if not self.redis:
                self.redis = await aioredis.from_url(settings.redis_url)

            client_ip = request.client.host if request.client else "unknown"
            key = f"rate_limit:{client_ip}"
            now = int(time.time())
            window = now // self.window_seconds
            redis_key = f"{key}:{window}"

            count = await self.redis.incr(redis_key)
            if count == 1:
                await self.redis.expire(redis_key, self.window_seconds)

            if count > self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            return await call_next(request)
        except aioredis.RedisError as e:
            raise HTTPException(status_code=500, detail="Redis connection error") from e
        finally:
            if self.redis:
                await self.redis.close()
