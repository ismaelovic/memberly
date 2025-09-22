from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class CommunicationTemplate(Base):
    __tablename__ = "communication_templates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[Text] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        nullable=True
    )  # Optional description of the template
