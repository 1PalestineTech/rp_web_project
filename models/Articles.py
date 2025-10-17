from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
from sqlalchemy import String
from moderls import db,categories

class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    desciption: Mapped[str] = mapped_column(String(128), nullable=False)
    avatar: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Relationship: One user -> many pages
    writer_id: Mapped[int | None] = mapped_column(ForeignKey("writers.id"))
    author: Mapped["Writer"] = relationship("Writer", back_populates="pages")
    actions: Mapped[list["Action"]] = relationship("Action", back_populates="target_article")

    tags = db.relationship(
        'Tag',
        secondary=categories,
        back_populates='articles'
    )