from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
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
    confirmed: Mapped[int] = mapped_column(Integer, default=0)
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
            "confirmed": self.confirmed,
            "token": self.token
        }


class NewsletterSubs(db.Model):
    __tablename__ = "newsletter_subs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    confirmed: Mapped[int] = mapped_column(Integer, default=0)
    token: Mapped[str] = mapped_column(String, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "confirmed": self.confirmed,
            "token": self.token
        }


class TopMovies(db.Model):
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


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(150))
    confirmed: Mapped[int] = mapped_column(Integer, default=0)
    token: Mapped[str] = mapped_column(String, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "confirmed": self.confirmed,
            "token": self.token
        }


def create_all(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app.run(debug=True)