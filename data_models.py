from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, foreign, backref, relationship

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    birth_date: Mapped[int] = mapped_column()
    death_date: Mapped[int] = mapped_column()

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column()
    publication_year: Mapped[int] = mapped_column()
    book_cover: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(db.ForeignKey("author.id"))
    author: Mapped["Author"] = relationship("Author", backref="books")


