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

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')
app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
