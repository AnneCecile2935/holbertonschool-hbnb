"""
Module review.py

Defines the Review class, which models a review left by a User for a Place.
Each review includes a textual comment, a rating (from 1 to 5),
a reference to the Place being reviewed (by ID), and the User who authored
it (by ID).

The class ensures validation of:
- text: must be a non-empty string,
- rating: must be an integer between 1 and 5,
- place: must be an object with an `id` attribute,
- user: must be an object with an `id` attribute.

The review is automatically added to the Place's list of reviews upon
initialization if `place.add_review()` is defined.
"""

from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property

class Review(BaseModel):
    """
    Review class represents a review made by a user on a place.

    Attributes:
        text (str): The content of the review. Cannot be empty.
        rating (int): Rating given to the place, must be between 1 and 5.
        place (str): ID of the place being reviewed. The place must be
        an object with an `id`.
        user (str): ID of the user who wrote the review. The user must be
        an object with an `id`.
    """
    __tablename__= 'reviews'                     # Création de la table 'reviews'
# ----------------------------------- Création des colonnes de la table reviews
# Relier les attributs privés aux colonnes de la BDD avec paramètres
    _text = db.Column(
        db.String(),
        nullable=False)
    _rating = db.Column(
        db.Integer(),
        nullable=False)

    place_id = db.Column(
        db.String(),
        db.ForeignKey("places.id"),
        nullable=False)
    user_id = db.Column(
        db.String(),
        db.ForeignKey("users.id"),
        nullable=False)
# --------------------------------------- Définition des attributs de la classe
    def __init__(self, text, rating, place, user):
        """
        Initializes a new Review instance.

        Args:
            text (str): The content of the review.
            rating (int): The rating score, must be between 1 and 5.
            place (Place): The Place object being reviewed.
            user (User): The User object who wrote the review.

        Raises:
            TypeError: If any argument is of an incorrect type.
            ValueError: If text is empty or rating is out of the valid range.
        """

        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        return (
            f"\nReview = (\n"
            f" text = {self.text},\n"
            f" rating = {self.rating},\n"
            f" place = {self.place_id},\n"
            f" user = {self.user_id},\n"
            f" created_at = {self.created_at}\n,"
            f" updated_at = {self.updated_at}\n)"
        )
# ------------------------------------------------------------- Gestion du text
    @hybrid_property
    def text(self):
        """
        str: The content of the review.

        Raises:
            TypeError: If assigned value is not a string.
            ValueError: If assigned value is an empty string.
        """
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise TypeError("the text must be a string")
        self._text = value.strip()
# ----------------------------------------------------------- Gestion du rating
    @hybrid_property
    def rating(self):
        """
        int: The rating given to the place, must be between 1 and 5.

        Raises:
            TypeError: If assigned value is not an integer.
            ValueError: If assigned value is not in [1, 5].
        """
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be a number")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
# --------------------------------------------------------- Gestion de la place
    @hybrid_property
    def place(self):
        """
        Place: Gets or sets the place being reviewed.

        Raises:
            TypeError: If the value is not a Place instance or does
            not have an 'id' attribute.
        """
        return self.place_id

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not hasattr(value, "id"):
            raise TypeError("The place must be an object Place with an id")
        self.place_id = value.id
# ------------------------------------------------------------ Gestion du title
    @hybrid_property
    def user(self):
        """
        User: Gets or sets the user who wrote the review.

        Raises:
            TypeError: If the value does not have an 'id' attribute.
        """
        return self.user_id

    @user.setter
    def user(self, value):
        if not hasattr(value, "id"):
            raise TypeError("user must be an object with an id")
        self.user_id = value.id
