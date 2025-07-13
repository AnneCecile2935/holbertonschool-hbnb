"""Defines the Review model for user feedback on places."""
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import CheckConstraint
from app.extensions import db
from .base_model import BaseModel


class Review(BaseModel):
    """Review model storing text, rating, and foreign keys to User and Place."""
    __tablename__ = 'reviews'                  # Création de la table 'reviews'
# ----------------------------------- Création des colonnes de la table reviews
    _text = db.Column(                      # Création de la colonne 'text'
        db.String(),                        # Value = String
        nullable=True)                     # Peux être NULL

    _rating = db.Column(                    # Création de la colonne 'rating'
        'rating',
        db.Integer(),                       # Value = Integer
        nullable=False)                     # Ne peux pas être NULL

    place_id = db.Column(                   # Création de la colonne 'place_id'
        db.String(),                        # Value = String
        db.ForeignKey("places.id"),         # Relie Review à places.id
        nullable=False)                     # Ne peux pas être NULL

    user_id = db.Column(                    # Création de la colonne 'user_id'
        db.String(),                        # Value = String
        db.ForeignKey("users.id"),          # Relie Review à users.id
        nullable=False)                     # Ne peux pas être NULL

    user = db.relationship(                 # Lien avec User
        "User",                             # Nom de la classe liée
        back_populates="reviews")           # Nom de la liste dans User

    place = db.relationship(                # Lien avec Place
        "Place",                            # Nom de la classe liée
        back_populates="reviews")           # Nom de la liste dans Place

    __table_args__ = (                      # Vérification des données SQL
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),)

# --------------------------------------- Définition des attributs de la classe
    def __init__(self, text, rating, place, user):
        """Initialize a Review instance with text, rating, user and place."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_obj = place
        self.user_obj = user

# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        """Return a readable string representation of the Review."""
        return (
            f"\nReview = (\n"
            f" text = {self.text},\n"
            f" rating = {self.rating},\n"
            f" place = {self.place_id},\n"
            f" user = {self.user_id},\n"
            f" created_at = {self.created_at},\n"
            f" updated_at = {self.updated_at}\n)"
        )

# ------------------------------------------------------------- Gestion du text
    @hybrid_property
    def text(self):
        """Return the review text."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the review text, must be a non-empty string."""
        # Vérifie que value est bien une string
        if not isinstance(value, str) or not value.strip():
            raise TypeError("the text must be a string")

        # Si tout est OK passe value à l'attribut 'text'
        self._text = value.strip()

# ----------------------------------------------------------- Gestion du rating
    @hybrid_property
    def rating(self):
        """Return the review rating (1 to 5)."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating, must be an integer between 1 and 5."""
        # Vérifie si la valeur est bien un integer
        if not isinstance(value, int):
            raise TypeError("Rating must be a number")

        # Vérifie que la valeur est bien comprise entre 1 et 5
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")

        # Si tout est OK passe value à l'attribut 'rating'
        self._rating = value

# --------------------------------------------------------- Gestion de la place
    @hybrid_property
    def place_obj(self):
        """Return the related Place ID."""
        return self.place_id

    @place_obj.setter
    def place_obj(self, value):
        """Set the related place, must be a Place instance with an ID."""
        # Vérifie que l'id de la place est bien attribué dans la BDD
        if not hasattr(value, "id"):
            raise TypeError("The place must be an object Place with an id")

        # Si tout est OK passe value à l'attribut 'place_id'
        self.place_id = value.id

# ------------------------------------------------------------ Gestion du title
    @hybrid_property
    def user_obj(self):
        """Return the related User ID."""
        return self.user_id

    @user_obj.setter
    def user_obj(self, value):
        """Set the related user, must be a User instance with an ID."""
        # Vérifie que l'id du user est bien attribué dans la BDD
        if not hasattr(value, "id"):
            raise TypeError("user must be an object with an id")

        # Si tout est OK passe value à l'attribut 'user_id'
        self.user_id = value.id
