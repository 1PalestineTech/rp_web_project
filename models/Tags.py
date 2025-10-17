from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
from sqlalchemy import String
from moderls import db,categories

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    articles = db.relationship(
        'Article',
        secondary=categories,
        back_populates='tags'
    )