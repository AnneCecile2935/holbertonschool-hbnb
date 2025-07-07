"""
This module defines the Amenity class, representing an equipment or service
that can be associated with a place (e.g., Wi-Fi, parking, etc.).

The class inherits from BaseModel, which provides a unique ID as well as
timestamps for creation and last update.
"""
from .base_model import BaseModel
from part3.app.extensions import db, bcrypt, jwt

class Amenity(BaseModel):
    """
    Class representing a facility or service available in a place.

    Attributes:
        name (str): Name of the amenity (required, max 50 characters).
    """
    amenities_name = {}

    def __init__(self, name):
        """
        Initializes a new Amenity instance.

        Args:
            name (str): Name of the amenity.
        """
        super().__init__()
        self.name = name

    def __repr__(self):
        """
        Returns a human-readable string representation of the amenity.
        """
        return f"Amenity = (\n id={self.id},\n name={self.name})"

    @property
    def name(self):
        """
        Returns the name of the amenity.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Sets the name of the amenity after validating type and length.

        Raises:
            TypeError: If value is not a non-empty string.
            ValueError: If value exceeds 50 characters.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name is too long, more than 50 characters")
        if value in Amenity.amenities_name and Amenity.amenities_name[value] is not self:
            raise ValueError("This amenity is already registered.")
        old_name = getattr(self, "_name", None)
        if old_name and old_name in Amenity.amenities_name:
            del Amenity.amenities_name[old_name]

        self._name = value
        Amenity.amenities_name[value] = self
