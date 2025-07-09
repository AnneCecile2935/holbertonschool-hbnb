"""
This module defines the Amenity class, representing an equipment or service
that can be associated with a place (e.g., Wi-Fi, parking, etc.).

The class inherits from BaseModel, which provides a unique ID as well as
timestamps for creation and last update.
"""
from .base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db

class Amenity(BaseModel):
    """
    Class representing a facility or service available in a place.

    Attributes:
        name (str): Name of the amenity (required, max 50 characters).
    """
    __tablename__ = 'amenities'              # Création de la table 'amenities'
# --------------------------------- Création des colonnes de la table amenities
# Relier les attributs privés aux colonnes de la BDD avec paramètres
    _name = db.Column(
        db.String(50),
        nullable=False,
        unique=True)

# --------------------------------------- Définition des attributs de la classe
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
        return (
            f"\nAmenity = (\n"
            f" id = {self.id},\n"
            f" name = {self.name},\n"
            f" created_at = {self.created_at},\n"
            f" updated_at = {self.updated_at}\n)")

    @hybrid_property
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

        existing = Amenity.query.filter_by(_name=value).first()
        if existing and existing.id != self.id:
            raise ValueError("This amenity is already registered.")

        self._name = value

