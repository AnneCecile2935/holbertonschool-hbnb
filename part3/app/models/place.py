"""
This module defines the Place class, representing a location available
for booking.
Each instance includes information such as title, description, nightly price,
geographic coordinates, the owner (a User instance), and associated collections
of reviews and amenities.

The class inherits from BaseModel, which provides a unique identifier
and timestamps for creation and updates.
"""
from .base_model import BaseModel
from part3.app.extensions import db, bcrypt, jwt

class Place(BaseModel):
    """
    Class representing a place in the HBnB application.

    Attributes:
        title (str)       : Title of the place (required, max 100 characters).
        description (str) : Optional description of the place.
        price (float)     : Nightly price (must be positive).
        latitude (float)  : Latitude coordinate (between -90.0 and 90.0).
        longitude (float) : Longitude coordinate (between -180.0 and 180.0).
        owner (str)       : ID of the user who owns the place.
        reviews (list)    : List of Review objects related to the place.
        amenities (list)  : List of Amenity objects available at the place.
    """
    place_list = {}

    def __init__(self, title, price, latitude,
                 longitude, owner, description=None):
        """
        Initializes a new Place instance with the given attributes.

        Args:
            title (str)       : Title of the place.
            description (str) : Description of the place.
            price (float)     : Nightly price (> 0).
            latitude (float)  : Latitude coordinate (-90.0 ≤ x ≤ 90.0).
            longitude (float) : Longitude coordinate (-180.0 ≤ x ≤ 180.0).
            owner (User)      : User instance who owns the place.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def __repr__(self):
        return (
            f"\nPlace = (\n"
            f" id = {self.id},\n"
            f" title = {self.title},\n"
            f" description = {self.description},\n"
            f" price = {self.price},\n"
            f" latitude = {self.latitude},\n"
            f" longitude = {self.longitude},\n"
            f" owner = {self.owner},\n"
            f" reviews = {self.reviews},\n"
            f" amenities = {self.amenities}\n,"
            f" created_at = {self.created_at}\n,"
            f" update_at = {self.update_at}\n)"
        )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Vérifie le type de donnée et si la donnée est vide
        if not isinstance(value, str) or not value.strip():
            raise TypeError("Title must be a non-empty string.")
        elif len(value) > 100:
            raise ValueError("Title must not exceed 100 characters.")
        else:
            self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # Vérifie le type de donnée et si la donnée est vide
        if not (isinstance(value, str) or value is None):
            raise TypeError("Description must be a string.")
        else:
            self._description = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        elif value <= 0:
            raise ValueError("Price must be a positive float.")
        else:
            self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a float.")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a float.")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self._longitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        # Vérifie que l'objet a un attribut id
        if not hasattr(value, "id"):
            raise TypeError(
                "Owner must be a User object with a valid ID."
            )
        self._owner = value.id

    def add_review(self, review):
        """
        Adds a review to the list of reviews for this place.

        Args:
            review (Review): A Review object to associate with the place.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Adds an amenity to the list of amenities for this place.

        Args:
            amenity (Amenity): An Amenity object to associate with the place.
        """
        self.amenities.append(amenity)
