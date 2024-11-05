# Centralized Database for Flask Applications Using SQLAlchemy

## Features

- Centralized database management for multiple Flask applications.
- Easy integration with SQLAlchemy ORM.
- Support for database migrations using Flask-Migrate.
- Environment variable configuration for sensitive data.

## Requirements

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/timonrieger/database-service.git
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add your configuration settings. Use the external database URL provided by your hosting service. Ensure that all applications interacting with the database use the same connection string:
    ```env
    SECRET=your_secret_key
    DB_URI=your_database_uri
    ```

## Usage

### 1. Importing the Database in Your Flask App

To initialize the database, import the database module and import the `db`, the `create_all` initializer method, and all tables you need in your application. Here’s how to set it up:

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

### 2. Migrations

Consider using Flask-Migrate for managing database schema changes.

Install Flask-Migrate:
```bash
pip install Flask-Migrate
```

Set up Flask-Migrate in your application:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

Run the following commands to initialize and apply migrations:
```bash
flask db init
flask db stamp head
flask db migrate
flask db upgrade
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
