"""Place model representing a rentable location with owner,
amenities, and reviews."""
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from .place_amenity import place_amenity
from .base_model import BaseModel


class Place(BaseModel):
    """Place table with fields for title, description, price,
    coordinates, and relations."""
    __tablename__ = 'places'                    # Création de la table 'places'
# ------------------------------------ Création des colonnes de la table places
    _title = db.Column(                  # Création de la colonne 'title'
        db.String(100),                  # Value = String -> 100 char max
        nullable=False)                  # Ne peux pas être NULL

    _description = db.Column(            # Création de la colonne 'description'
        db.String(),                     # Value = String
        nullable=True)                   # Peux être NULL

    _price = db.Column(                  # Création de la colonne 'price'
        "_price",                         # Nom pour les checkContraint
        db.Float(),                      # Value = Float
        nullable=False)                  # Ne peux pas être NULL

    _latitude = db.Column(               # Création de la colonne 'latitude'
        "_latitude",                      # Nom pour les checkContraint
        db.Float(),                      # Value = Float
        nullable=False)                  # Ne peux pas être NULL

    _longitude = db.Column(              # Création de la colonne 'longitude'
        "_longitude",                     # Nom pour les checkContraint
        db.Float(),                      # Value = Float
        nullable=False)                  # Ne peux pas être NULL

    owner_id = db.Column(                # Création de la colonne 'owner_id'
        db.String(),                     # Value = String
        db.ForeignKey("users.id"),       # Relie Place à users.id
        nullable=False)                  # Ne peux pas être NULL

    reviews = relationship(              # Lien avec Review
        "Review",                        # Nom de la classe liée
        back_populates="place",          # Nom de la liste dans Review
        cascade="all, delete-orphan")    # Gestion de la récupération et delete

    amenities = db.relationship(         # Lien avec Amenity
        "Amenity",                       # Nom de la classe liée
        secondary=place_amenity,         # Nom de la table secondaire
        back_populates="places",         # Nom de la liste dans Amenity
        cascade="all")                   # Gestion de la récupération

    __table_args__ = (                   # Vérification des données SQL
        CheckConstraint(
            '_price > 0',
            name='check_positive_price'),
        CheckConstraint(
            '_latitude >= -90 AND _latitude <= 90',
            name='check_latitude_range'),
        CheckConstraint(
            '_longitude >= -180 AND _longitude <= 180',
            name='check_longitude_range'))

# --------------------------------------- Définition des attributs de la classe
    def __init__(self, title, price, latitude,
                 longitude, owner, description=None):
        """Initialize Place with required fields and optional description."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id

# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        """String representation of a Place instance."""
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
            f" amenities = {self.amenities},\n"
            f" created_at = {self.created_at},\n"
            f" updated_at = {self.updated_at}\n)")

# ------------------------------------------------------------ Gestion du title
    @hybrid_property
    def title(self):
        """Title of the place."""
        return self._title

    @title.setter
    def title(self, value):
        """Title of the place."""
        # Vérifie le type de donnée et si la donnée est vide
        if not isinstance(value, str) or not value.strip():
            raise TypeError("Title must be a non-empty string.")
        # Vérifie le nb de caractères de la string
        elif len(value) > 100:
            raise ValueError("Title must not exceed 100 characters.")
        # Sinon return la valeur nettoyée
        else:
            self._title = value.strip()

# --------------------------------------------------- Gestion de la description
    @hybrid_property
    def description(self):
        """Optional textual description of the place."""
        return self._description

    @description.setter
    def description(self, value):
        """Optional textual description of the place."""
        # Vérifie si value est différente de None
        if value is not None:
            # Vérifie que value est une string
            if not isinstance(value, str):
                raise TypeError("Description must be a string.")

            # Supprime les espaces en début/fin de chaîne
            value = value.strip()

            # Si la string est vide après nettoyage -> passe à None
            if value == "":
                self._description = None
            # Si pleine ont passe la value à l'attribut 'description'
            else:
                self._description = value
        else:
            # Si value est None, on l'assigne tel quel
            self._description = None

# ------------------------------------------------------------ Gestion du price
    @hybrid_property
    def price(self):
        """Rental price of the place (positive float)."""
        return self._price

    @price.setter
    def price(self, value):
        """Rental price of the place (positive float)."""
        # Vérifie si la value est un integer ou un float
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        # Vérifie si la value est positive
        elif value <= 0:
            raise ValueError("Price must be a positive float.")
        # Si tout est OK passe value en float et à l'attribut 'price'
        else:
            self._price = float(value)

# ------------------------------------------------------ Gestion de la latitude
    @hybrid_property
    def latitude(self):
        """Latitude coordinate (-90.0 to 90.0)."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Latitude coordinate (-90.0 to 90.0)."""
        # Vérifie si la value est un integer ou un float
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a float.")
        # Vérifie que la value est bien comprise en -90 et 90
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        # Si tout est OK passe value en float et à l'attribut 'latitude'
        self._latitude = float(value)

# ----------------------------------------------------- Gestion de la longitude
    @hybrid_property
    def longitude(self):
        """Longitude coordinate (-180.0 to 180.0)."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Longitude coordinate (-180.0 to 180.0)."""
        # Vérifie si la value est un integer ou un float
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a float.")
        # Vérifie que la value est bien comprise en -180 et 180
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        # Si tout est OK passe value en float et à l'attribut 'longitude'
        self._longitude = float(value)

# ------------------------------------------------------------ Gestion du owner
    @hybrid_property
    def owner(self):
        """User who owns the place (linked via foreign key)."""
        return self.owner_id

    @owner.setter
    def owner(self, value):
        """User who owns the place (linked via foreign key)."""
        # Vérifie que l'objet a un attribut id
        if not hasattr(value, "id"):
            raise TypeError(
                "Owner must be a User object with a valid ID."
            )
        # Si tout est OK passe value à l'attribut 'owner_id'
        self.owner_id = value.id
