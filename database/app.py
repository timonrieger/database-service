from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import Integer, String, Float, DateTime, Text, func, Boolean
from typing import List
from flask_migrate import Migrate
from flask import Flask 
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET'] = os.getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Base(DeclarativeBase):
    pass


class AirNomads(Base):
    __tablename__ = "air_nomads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    departure_city: Mapped[str] = mapped_column(String)
    departure_iata: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String)
    min_nights: Mapped[int] = mapped_column(Integer)
    max_nights: Mapped[int] = mapped_column(Integer)
    travel_countries: Mapped[str] = mapped_column(String)
    token: Mapped[str] = mapped_column(String, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "departure_city": self.departure_city,
            "departure_iata": self.departure_iata,
            "currency": self.currency,
            "min_nights": self.min_nights,
            "max_nights": self.max_nights,
            "travel_countries": self.travel_countries,
            "token": self.token 
        }


class TopMovies(Base):
    __tablename__ = "top_movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review: Mapped[str] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "description": self.description,
            "rating": self.rating,
            "review": self.review,
            "img_url": self.img_url
        }


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150), unique=True)
    confirmed: Mapped[int] = mapped_column(Integer, default=0)
    token: Mapped[str] = mapped_column(String, unique=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    apikey: Mapped[str] = mapped_column(String, nullable=True)
    blog_posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="author")
    blog_comments: Mapped[List["BlogComment"]] = relationship("BlogComment", back_populates="comment_author")
    type: Mapped[str] = mapped_column(String(50), default=os.urandom(50))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        "polymorphic_on": "type"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "confirmed": self.confirmed,
            "token": self.token,
            "admin": self.admin,
            "apikey": self.apikey,
            "blog_posts": self.blog_posts,
            "blog_comments": self.blog_comments
        }
        
        
class Ressources(Base):
    __tablename__ = "ressources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    medium: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[str] = mapped_column(String, default=json.dumps([]))
    user_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("users.id"))
    added: Mapped[datetime] = mapped_column(DateTime, default=func.current_timestamp(), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "medium": self.medium,
            "category": self.category,
            "tags": self.tags,
            "user_id": self.user_id,
            "added": self.added,
            "description": self.description,
            "private": self.private
        }


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Relationships
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="blog_posts")
    comments: Mapped[List["BlogComment"]] = relationship("BlogComment", back_populates="parent_post")


class BlogComment(Base):
    __tablename__ = "blog_comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)
    # Relationships
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author: Mapped["User"] = relationship("User", back_populates="blog_comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")



def create_all(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
