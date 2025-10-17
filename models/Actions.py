from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
from sqlalchemy import String
from moderls import db
from sqlalchemy.sql import func

class Action(db.Model):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    date: Mapped[str] = db.Column(db.DateTime(timezone=True), server_default=func.now())

    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id"))
    admin: Mapped["Admin"] = relationship("Admin", back_populates="actions")

    writer_id: Mapped[int | None] = mapped_column(ForeignKey("writers.id"))
    writer: Mapped["Writer"] = relationship("Writer", back_populates="actions")

    article_id: Mapped[int | None] = mapped_column(ForeignKey("articles.id"))
    article: Mapped["Article"] = relationship("Article", back_populates="actions")