from datetime import datetime as dt
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, Text, func, Boolean, ForeignKey
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


class AirNomads(db.Model):
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
    excluded_countries: Mapped[str] = mapped_column(String, server_default="")
    token: Mapped[str] = mapped_column(String, unique=True)
    min_days_ahead: Mapped[int] = mapped_column(Integer, server_default="1")
    max_days_ahead: Mapped[int] = mapped_column(Integer, server_default="182")


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
            "excluded_countries": self.excluded_countries,
            "token": self.token,
            "min_days_ahead": self.min_days_ahead,
            "max_days_ahead": self.max_days_ahead
        }


class TopMovies(db.Model):
    __tablename__ = "top_movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review: Mapped[str] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "year": self.year,
            "description": self.description,
            "rating": self.rating,
            "review": self.review,
            "img_url": self.img_url
        }


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150), unique=True)
    confirmed: Mapped[int] = mapped_column(Integer, default=0)
    token: Mapped[str] = mapped_column(String, unique=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    apikey: Mapped[str] = mapped_column(String, nullable=True)

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
        }
        
        
class Ressources(db.Model):
    __tablename__ = "ressources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    medium: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[str] = mapped_column(String, default=json.dumps([]))
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id"))
    added: Mapped[dt] = mapped_column(DateTime, default=func.current_timestamp())
    description: Mapped[str] = mapped_column(String, nullable=True)
    private: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "medium": self.medium,
            "category": self.category,
            "tags": self.tags,
            "user_id": self.user_id,
            "added": self.added.isoformat(),
            "description": self.description,
            "private": self.private
        }


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    create_date: Mapped[dt] = mapped_column(DateTime, nullable=False)
    edit_date: Mapped[dt] = mapped_column(DateTime, nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_draft: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[str] = mapped_column(String, default=json.dumps([]))
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comments: Mapped[List["BlogComment"]] = relationship("BlogComment", back_populates="parent_post")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "create_date": self.create_date.isoformat(),
            "edit_date": self.edit_date.isoformat() if self.edit_date else None,
            "body": self.body,
            "img_url": self.img_url,
            "deleted": self.deleted,
            "is_draft": self.is_draft,
            "tags": self.tags,
            "author_id": self.author_id
        }


class BlogComment(db.Model):
    __tablename__ = "blog_comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    create_date: Mapped[dt] = mapped_column(DateTime, nullable=False)
    edited: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "create_date": self.create_date.isoformat(),
            "edited": self.edited,
            "deleted": self.deleted,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


def create_all(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
