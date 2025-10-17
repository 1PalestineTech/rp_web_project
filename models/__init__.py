from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

categories = db.Table(
    'category',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)