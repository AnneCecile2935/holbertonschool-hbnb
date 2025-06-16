"""
Initialization of the Flask application for the HBnB project - Part 2:
Authentication and Database.

This module defines the `create_app()` factory function, which initializes
the Flask application with the Flask-RESTX extension for building
a RESTful API.

Features:
- Creation of the main Flask application instance.
- Configuration of API documentation using Swagger UI at `/api/v1/`.
- Prepared structure for future resource namespaces:
    - users
    - places
    - reviews
    - amenities

To be implemented:
- Registration of API namespaces in the `Api` object.
- Integration of database and authentication extensions.
"""
from flask import Flask
from flask_restx import Api


def create_app():
    """
    Creates and configures the Flask application instance for the HBnB project.

    This function initializes:
    - The core Flask application.
    - The Flask-RESTX extension for auto-generated API documentation.
    - Base configuration of the API, including:
        - title
        - version
        - description
        - Swagger documentation path

    Note:
    - Resource namespaces will be added in future steps.

    Returns:
    - A configured Flask application instance.
    """
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for:
    # places
    # reviews
    # amenities will be added later

    return app
