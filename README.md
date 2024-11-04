# Using the `database-service` Database Repository in Your Flask Project

This guide will walk you through installing the `database-service` repository in your Flask project, calling the `create_db` function, and setting up a GitHub Action workflow to automatically listen for changes in the `database-service` repo, reinstall it, and push updates to your project.

## 1. Installing the `database-service` Database Repository

To install the `database-service` repository directly from GitHub, use the following command:

```bash
 pip install git+ssh://git@github.com/timonrieger/database-service.git
```

## 2. Calling the create_db Function

To initialize the database tables from the database repo within your Flask app, you need to call the create_db function. Here’s how to set it up:

```python
from flask import Flask
from database.models import db, create_db

def create_app():
    app = Flask(__name__)
    
    # Configure the database URI (replace with your database URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the shared database models with the Flask app
    db.init_app(app)
    
    with app.app_context():
        create_db(app)  # Calls create_db to create tables if they don't exist

    return app
```

## 3. Use Models in Your Flask App

You can now import and use the models from database-service in your routes and other parts of your Flask project.

```python
from databse import AirNomads, db
```
## 4. Best Practices

Environment Variables: Use a .env file or another method to store sensitive configurations like the SQLALCHEMY_DATABASE_URI.
Database Migrations: Consider using Flask-Migrate for managing database schema changes.
```bash
pip install Flask-Migrate
```
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```
```bash 
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
