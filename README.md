# Using the `shared_models` Database Repository in Your Flask Project

This guide will walk you through installing the `shared_models` repository in your Flask project, calling the `create_db` function, and setting up a GitHub Action workflow to automatically listen for changes in the `shared_models` repo, reinstall it, and push updates to your project.

## 1. Installing the `shared_models` Database Repository

To install the `shared_models` repository directly from GitHub, use the following command:

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

## 3. Setting Up a GitHub Action Workflow

Create a GitHub Actions workflow that listens for changes in the shared_models repository. When changes are detected, the workflow will reinstall the repository, commit the updated code, and push it to your Flask project.

```python
name: Update Database

on:
  push:
    branches:
      - main
    paths:
      - 'requirements.txt'
      - '.github/workflows/update_shared_models.yml'

  schedule:
    - cron: '0 0 * * *'  # Runs daily; adjust as needed

jobs:
  update-shared-models:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -U pip
        pip install git+ssh://git@github.com/yourusername/shared_models.git

    - name: Check for updates in shared models
      run: |
        # Check if there are changes in shared models after reinstallation
        if [ -n "$(git status --porcelain)" ]; then
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add .
          git commit -m "Update shared models"
          git push origin main
        else
          echo "No changes detected in shared models"
        fi
```

Explanation

	•	on section: Triggers the workflow when changes are pushed to the main branch or on a schedule.
	•	steps:
	•	Checkout repository: Checks out the repository’s code.
	•	Set up Python: Sets up a Python environment.
	•	Install dependencies: Installs the shared_models repository from GitHub.
	•	Check for updates: Commits and pushes changes if any updates are detected after reinstalling shared_models.

Best Practices

	•	Security: Use GitHub secrets for storing sensitive data like SSH keys or tokens for private repository access.
	•	Testing: Ensure you test the workflow in a development branch before deploying to production.

This setup helps keep your Flask project updated with the latest changes from the shared_models repo seamlessly.