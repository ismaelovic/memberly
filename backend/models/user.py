from sqlalchemy import BIGINT, ForeignKey
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
    PENDING = "pending"


class MemberGender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class MemberProfile(Base):
    __tablename__ = "member_profile"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    tenant_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    member_auth_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("member_auth.id", ondelete="CASCADE"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[datetime.date] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    zip_code: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[MemberGender] = mapped_column(nullable=False)

    auth = relationship("MemberAuth", back_populates="profile")
    memberships = relationship("Membership", back_populates="member")
    tenant = relationship("Tenant", back_populates="members")
    communications = relationship("Communication", back_populates="member")


class MemberAuth(Base):

    __tablename__ = "member_auth"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[Role] = mapped_column(nullable=False)
    state: Mapped[MemberState] = mapped_column(
        nullable=False, default=MemberState.ACTIVE
    )
    last_login: Mapped[datetime.datetime] = mapped_column(nullable=True)
    login_attempts: Mapped[int] = mapped_column(BIGINT, default=0, nullable=False)
    password_reset_token: Mapped[str] = mapped_column(nullable=True)
    password_reset_expiry: Mapped[datetime.datetime] = mapped_column(nullable=True)

    profile = relationship("MemberProfile", back_populates="auth", uselist=False)
