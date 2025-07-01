"""
Module user.py

Defines the User class inheriting from BaseModel.
This class models a user with attributes like first name,
last name, email (unique and validated), and admin status.
Includes property setters with validation and email uniqueness
tracking across all User instances.
"""


from app.models.base_model import BaseModel

from datetime import datetime


class User(BaseModel):
    """
    User class inheriting from BaseModel.
    Represents a user with first name, last name, email, and admin status.
    Ensures email uniqueness and validity.
    """
    users_email = {}

    def __init__(
        self, first_name, last_name, email, user_password, is_admin=False
    ):
        """
        Initialize a new User instance.

        Args:
            first_name (str): User's first name. Cannot be empty or None.
            last_name (str): User's last name. Cannot be empty or None.
            email (str): User's email. Must be valid and unique.
            is_admin (bool): Whether the user has admin rights. Default False.

        Raises:
            ValueError: If first_name, last_name, or
            email are invalid or empty.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.place = []
        self.password = user_password

    def __repr__(self):
        return (
            f"\nUser = (\n"
            f" id = {self.id},\n"
            f" first_name = {self.first_name},\n"
            f" last_name = {self.last_name},\n"
            f" email = {self.email},\n"
            f" is_admin = {self.is_admin},\n"
            f" created_at = {self.created_at},\n"
            f" update_at = {self.update_at},\n"
            f")"
        )

    @property
    def first_name(self):
        """
        Get the user's first name.

        Returns:
            str: The user's first name.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """
        Set the user's first name.

        Args:
            value (str): New first name.

        Raises:
            TypeError: If value is not a string.
            ValueError: If empty or too long (> 50 chars).
        """
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")
        if not value or not value.strip():
            raise ValueError("first_name is required and cannot be empty")
        if len(value) > 50:
            raise ValueError(
                "first_name is too long, more than 50 characters"
            )
        self._first_name = value.strip()

    @property
    def last_name(self):
        """
        Get the user's last name.

        Returns:
            str: The user's last name.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """
        Set the user's last name.

        Args:
            value (str): New last name.

        Raises:
            ValueError: If empty or too long (> 50 chars).
        """
        if not value or not value.strip():
            raise ValueError("last_name is required and cannot be empty")
        if len(value) > 50:
            raise ValueError(
                "last_name is too long, more than 50 characters"
            )
        self._last_name = value.strip()

    @property
    def email(self):
        """
        Get the user's email address.

        Returns:
            str: The user's email.
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        Set the user's email address.

        Args:
            value (str): New email address.

        Raises:
            ValueError: If email is invalid or already used.

        """
        if not value or not value.strip():
            raise ValueError("email is required and cannot be empty")
        cleaned_email = value.strip()
        if not self.email_valid(cleaned_email):
            raise ValueError("Email format is invalid")
        if (cleaned_email in User.users_email and
                User.users_email[cleaned_email] is not self):
            raise ValueError("This email is already used")


        old_email = getattr(self, "_email", None)
        if old_email and old_email in User.users_email:
            del User.users_email[old_email]

        self._email = value.strip()
        User.users_email[cleaned_email] = self

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if type(value) is not bool:
            raise ValueError("Is_admin must be a boolean")
        self._is_admin = value

    @staticmethod
    def email_valid(email):
        """
        Validate the email format.

        Args:
            email (str): The email string to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if email.count('@') != 1:
            return False
        name, domain = email.split('@')
        if '.' not in domain:
            return False
        return True

    @property
    def password(self):
        """The password is write-only and cannot be read."""
        raise AttributeError("The password is not accessible in read")

    @password.setter
    def password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self._password_hash, password)


    def to_dict(self):
        """
        Convert the user object to a dictionary representation.

        Returns:
            dict: A dictionary containing user attributes:
                - 'id': User identifier
                - 'first_name': User's first name
                - 'last_name': User's last name
                - 'email': User's email address
                - 'is_admin': Boolean flag indicating admin status
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
