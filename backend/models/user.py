from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
import enum
import datetime


class Role(enum.Enum):
    SYSTEM_ADMIN = "system_admin"
    TENANT_ADMIN = "tenant_admin"
    STAFF = "staff"
    MEMBER = "member"


class MemberState(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    PAUSED = "paused"


class MemberProfile(Base):
    __tablename__ = "member_profile"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False)
    state: Mapped[MemberState] = mapped_column(
        nullable=False, default=MemberState.ACTIVE
    )

    auth = relationship("MemberAuth", back_populates="profile")


class MemberAuth(Base):

    __tablename__ = "member_auth"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    last_login: Mapped[datetime.datetime] = mapped_column(nullable=True)
    login_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    password_reset_token: Mapped[str] = mapped_column(nullable=True)
    password_reset_expiry: Mapped[datetime.datetime] = mapped_column(nullable=True)

    profile = relationship("MemberProfile", back_populates="auth")
