from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(100).with_variant(String(100, collation="utf8_unicode_ci"), "mysql"),
        nullable=False,
    )
    making_time: Mapped[str] = mapped_column(
        String(100).with_variant(String(100, collation="utf8_unicode_ci"), "mysql"),
        nullable=False,
    )
    serves: Mapped[str] = mapped_column(
        String(100).with_variant(String(100, collation="utf8_unicode_ci"), "mysql"),
        nullable=False,
    )
    ingredients: Mapped[str] = mapped_column(
        String(300).with_variant(String(300, collation="utf8_unicode_ci"), "mysql"),
        nullable=False,
    )
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )