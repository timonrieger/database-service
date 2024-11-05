# Centralized Database for flask applications using sqlalchemy

## 1. Installing the `database-service` Database Repository

To install the `database-service` repository directly from GitHub, use the following command:

```bash
 pip install git+ssh://git@github.com/timonrieger/database-service.git
```

## 2. Importing the database

To initialize the database import the database module and import the `db`, the `create_all` initilizer method and all tables you need in your application. 
Environment Variables: Use a .env file or another method to store sensitive configurations like the SQLALCHEMY_DATABASE_URI. Here’s how to set it up:

```python
from database import db, create_all, User
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config['SECRET'] = os.getenv("SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    create_all(app)
```

## 3. Migrations

Consider using Flask-Migrate for managing database schema changes.
```bash
pip install Flask-Migrate
```
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```
```bash 
flask db init
flask db migrate
flask db upgrade
```
