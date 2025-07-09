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
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from .liaison_table import place_amenity        # Import de la table de liaison
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
    __tablename__= 'places'                     # Création de la table 'places'
# ------------------------------------ Création des colonnes de la table places
# Relier les attributs privés aux colonnes de la BDD avec paramètres
    _title = db.Column(
        db.String(100),
        nullable=False)
    _description = db.Column(
        db.String(),
        nullable=True)
    _price = db.Column(
        db.Float(),
        nullable=False)
    _latitude = db.Column(
        db.Float(),
        nullable=False)
    _longitude = db.Column(
        db.Float(),
        nullable=False)

    owner_id = db.Column(
        db.String(),
        db.ForeignKey("users.id"),
        nullable=False)

    reviews = relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan")
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",
        cascade="all, delete")

    # Vérification des données SQL
    __table_args__ = (
        CheckConstraint(
            '_price > 0',
            name='check_positive_price'),
        CheckConstraint(
            '_latitude >= -90 AND _latitude <= 90',
            name='check_latitude_range'),
        CheckConstraint(
            '_longitude >= -180 AND _longitude <= 180',
            name='check_longitude_range'),
    )
# --------------------------------------- Définition des attributs de la classe
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
# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        return (
            f"\nPlace = (\n"
            f" id = {self.id},\n"
            f" title = {self.title},\n"
            f" description = {self.description},\n"
            f" price = {self.price},\n"
            f" latitude = {self.latitude},\n"
            f" longitude = {self.longitude},\n"
            f" owner = {self.owner_id},\n"
            f" reviews = {self.reviews},\n"
            f" amenities = {self.amenities}\n,"
            f" created_at = {self.created_at}\n,"
            f" updated_at = {self.updated_at}\n)"
        )

# ------------------------------------------------------------ Gestion du title
    @hybrid_property
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

# --------------------------------------------------- Gestion de la description
    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # Vérifie le type de donnée et si la donnée est vide
        if not (isinstance(value, str) or value is None):
            raise TypeError("Description must be a string.")
        if value is not None:
            self._description = value.strip()
        else:
            self._description = None
# ------------------------------------------------------------ Gestion du price
    @hybrid_property
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
# ------------------------------------------------------ Gestion de la latitude
    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a float.")
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self._latitude = float(value)
# ----------------------------------------------------- Gestion de la longitude
    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a float.")
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self._longitude = float(value)
# ------------------------------------------------------------ Gestion du owner
    @hybrid_property
    def owner(self):
        return self.owner_id

    @owner.setter
    def owner(self, value):
        # Vérifie que l'objet a un attribut id
        if not hasattr(value, "id"):
            raise TypeError(
                "Owner must be a User object with a valid ID."
            )
        self.owner_id = value.id
