from fastapi import FastAPI, Response, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel

from backend.api.member import router as member_router
from backend.api.membership import router as membership_router
from backend.api.communication import router as communication_router
from backend.api.payment import router as payment_router
from backend.api.auth import router as auth_router
from backend.api.subscriptions import router as subscription_router
from backend.api.admin import router as admin_router
from backend.core.config import settings
from backend.db.session import engine, get_db
from backend.models.user import MemberAuth
from backend.core.security import create_access_token, verify_password
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Membership Management System API",
    description="API for managing members, memberships, payments, and communications in a multi-tenant system.",
    version="1.0.0",
    contact={
        "name": "Support Team",
        "email": "support@membership-system.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "https://e6adec89c468.ngrok-free.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "ngrok-skip-browser-warning"],  # Add the custom header here
)

app.include_router(member_router, prefix="/api", tags=["Members"])
app.include_router(membership_router, prefix="/api", tags=["Memberships"])
app.include_router(communication_router, prefix="/api", tags=["Communications"])
app.include_router(payment_router, prefix="/api", tags=["Payments"])
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(subscription_router, prefix="/api", tags=["Subscriptions"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Membership Management System!"}


@app.on_event("startup")
async def startup_event():
    # Log useful startup information
    db_url = settings.database_url
    db_name = db_url.split("/")[-1] if db_url else "Unknown"
    env = "Development" if settings.debug else "Production"
    print(f"[INFO] Starting server in {env} mode")
    print(f"[INFO] Connected to database: {db_name}")


@app.on_event("shutdown")
async def shutdown_event():
    print("[INFO] Shutting down server...")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
