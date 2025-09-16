from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.pool import QueuePool
from contextvars import ContextVar
from typing import Optional, Generator
from backend.core.config import settings

# from db.base import Base

# Context variable for tenant schema
_tenant_schema_ctx: ContextVar[Optional[str]] = ContextVar(
    "tenant_schema", default=None
)

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=settings.debug,
    future=True,
)

# Scoped session factory
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def set_tenant_schema(schema: str):
    _tenant_schema_ctx.set(schema)


def get_tenant_schema() -> Optional[str]:
    return _tenant_schema_ctx.get()


# Set PostgreSQL search_path for multi-tenancy
@event.listens_for(Session, "before_flush")
def set_search_path(session, flush_context, instances):
    schema = get_tenant_schema()
    if schema:
        session.execute(text(f"SET search_path TO {schema}, public"))


# Health check utility
def db_health_check() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
