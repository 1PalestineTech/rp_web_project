from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from moderls import db

class Writer(db.Model):
    __tablename__ = "writers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    # Relationship: One user -> many pages
    pages: Mapped[list["Article"]] = relationship("Article", back_populates="author")
    actions: Mapped[list["Action"]] = relationship("Action", back_populates="target_writer")