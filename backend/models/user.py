from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from backend.core.security import hash_password
from backend.schemas.auth import RegisterRequest, MemberGender, MemberState, Role
from .base import Base
import datetime


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


def create_user(db: Session, user_data: RegisterRequest, tenant_id):
    hashed_password = hash_password(user_data.password)
    user = MemberAuth(
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        state=user_data.state,
        login_attempts=0,
    )
    db.add(user)
    db.flush()  # Ensure the user ID is generated

    profile = MemberProfile(
        tenant_id=tenant_id,
        member_auth_id=user.id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        birthday=user_data.date_of_birth,
        gender=user_data.gender,
        address=user_data.address,
        zip_code=user_data.zip_code,
        phone_number=user_data.phone,
    )
    db.add(profile)
    return True
