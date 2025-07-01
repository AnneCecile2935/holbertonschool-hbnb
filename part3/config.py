"""
Application configuration module for HBnB (Part 2).

This file defines the base configuration class and environment-specific
settings (e.g., development mode). The configuration is used to control
Flask behavior, including debug mode and secret key management.

Environment variable:
- SECRET_KEY: Overrides the default secret key if set.
"""
import os


class Config:
    """
    Base configuration class.

    Attributes:
    - SECRET_KEY: Used for session management and security features.
    - DEBUG: Set to False by default.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development-specific configuration.

    Inherits from the base Config class and enables debug mode.
    """
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
