from fastapi import FastAPI
from backend.api.member import router as member_router
from backend.api.membership import router as membership_router
from backend.api.communication import router as communication_router
from backend.api.payment import router as payment_router
from backend.core.config import settings
from backend.db.session import engine

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

app.include_router(member_router, prefix="/api", tags=["Members"])
app.include_router(membership_router, prefix="/api", tags=["Memberships"])
app.include_router(communication_router, prefix="/api", tags=["Communications"])
app.include_router(payment_router, prefix="/api", tags=["Payments"])


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
