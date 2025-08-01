"""
Entry point for the HBnB application (Part 2).

This script initializes the Flask application using the `create_app()` factory
and starts the development server with debug mode enabled.

Usage:
-------
$ python run.py

Note:
------
Debug mode should only be used during local development.
"""
import logging
from app import create_app
from app.extensions import db
from app.models import user

logging.basicConfig(
    level=logging.INFO,  # Niveau de log : DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Envoie les logs vers le terminal
    ]
)
app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
