from fastapi import FastAPI, Response, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from backend.api.member import router as member_router
from backend.api.membership import router as membership_router
from backend.api.communication import router as communication_router
from backend.api.payment import router as payment_router
from backend.core.config import settings
from backend.db.session import engine, get_db
from backend.models import User
from backend.core.security import create_access_token, verify_password

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


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.post("/auth/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email},
        roles=user.roles,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"message": "Login successful"}


@app.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@app.get("/auth/validate")
def validate_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Token validation logic here
    return {"message": "Token is valid"}
