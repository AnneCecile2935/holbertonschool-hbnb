"""
Initialization of the service layer for the HBnB application.

This module imports and instantiates the `HBnBFacade`, which centralizes access
to the core business logic of the application, including:
- users
- places
- reviews
- amenities

The `facade` object can then be used throughout the application (API routes,
controllers, etc.) to interact with the business services in a unified way.
"""
from app.services.facade import HBnBFacade


facade = HBnBFacade()
