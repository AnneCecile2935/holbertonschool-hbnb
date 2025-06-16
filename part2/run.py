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
from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
