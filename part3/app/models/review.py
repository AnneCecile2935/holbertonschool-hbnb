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

from part3.app.extensions import db, bcrypt, jwt
from app.models.base_model import BaseModel
from app.models.user import User


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
    reviews_list = {}

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

        place.add_review(self)

    def __repr__(self):
        return (
            f"\nReview = (\n"
            f" text = {self.text},\n"
            f" rating = {self.rating},\n"
            f" place = {self.place},\n"
            f" user = {self.user},\n"
            f" created_at = {self.created_at}\n,"
            f" update_at = {self.update_at}\n)"
        )

    @property
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

    @property
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

    @property
    def place(self):
        """
        Place: Gets or sets the place being reviewed.

        Raises:
            TypeError: If the value is not a Place instance or does
            not have an 'id' attribute.
        """
        return self._place

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not hasattr(value, "id"):
            raise TypeError("The place must be an object Place with an id")
        self._place = value.id

    @property
    def place_id(self):
        return self._place

    @property
    def user(self):
        """
        User: Gets or sets the user who wrote the review.

        Raises:
            TypeError: If the value does not have an 'id' attribute.
        """
        return self._user

    @user.setter
    def user(self, value):
        if not hasattr(value, "id"):
            raise TypeError("user must be an object with an id")
        self._user = value.id

    @property
    def user_id(self):
        return self._user



