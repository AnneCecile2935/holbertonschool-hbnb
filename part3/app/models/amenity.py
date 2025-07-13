"""Defines the Amenity model (name only)."""
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model with unique name field."""
    __tablename__ = 'amenities'              # Création de la table 'amenities'
# --------------------------------- Création des colonnes de la table amenities
    _name = db.Column(                          # Création de la colonne 'name'
        db.String(50),                          # Value = String -> 50 char max
        nullable=False,                         # Ne peux pas être NULL
        unique=True)                            # Doit être unique

# --------------------------------------- Définition des attributs de la classe
    def __init__(self, name):
        """Initialize Amenity with a name."""
        super().__init__()
        self.name = name

# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        """String representation of the amenity."""
        return (
            f"\nAmenity = (\n"
            f" id = {self.id},\n"
            f" name = {self.name},\n"
            f" created_at = {self.created_at},\n"
            f" updated_at = {self.updated_at}\n)")

# ------------------------------------------------------------- Gestion du name
    @hybrid_property
    def name(self):
        """Get the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Validate and set the amenity name."""
        # Vérifie si la value est une string
        if not isinstance(value, str):
            raise TypeError("Name must be a string")

        # 'Nettoie' la valeur -> évite les espaces autour de value
        value = value.strip()

        # Vérifie si la valeur est vide
        if not value:
            raise ValueError("Name cannot be empty")
        # Vérifie que la value fait 50 char max
        if len(value) > 50:
            raise ValueError("Name is too long, more than 50 characters")

        # Recherche du nom de l'amenity dans la BDD
        existing = Amenity.query.filter_by(_name=value).first()

        # Vérifie que l'amenity n'existe pas déjà dans la BDD
        if existing and existing.id != self.id:
            raise ValueError("This amenity is already registered.")

        # Si tout est OK passe value à l'attribut 'name'
        self._name = value
