"""
Module user.py

Defines the User class inheriting from BaseModel.
This class models a user with attributes like first name,
last name, email (unique and validated), and admin status.
Includes property setters with validation and email uniqueness
tracking across all User instances.
"""
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
import re                                       # Validation syntaxe de l'email


class User(BaseModel):
    """
    User class inheriting from BaseModel.
    Represents a user with first name, last name, email, and admin status.
    Ensures email uniqueness and validity.
    """
    __tablename__ = 'users'                      # Création de la table 'users'
# ------------------------------------- Création des colonnes de la table users
# Relier les attributs privés aux colonnes de la BDD avec paramètres
    _first_name = db.Column(
        db.String(50),
        nullable=False)
    _last_name = db.Column(
        db.String(50),
        nullable=False)
    _email = db.Column(
        db.String(120),
        nullable=False,
        unique=True)
    _password_hash = db.Column(
        db.String(128),
        nullable=False)
    _is_admin = db.Column(
        db.Boolean,
        default=False)

    places = relationship(              # Relation entre le user et ses places
    "Place",
    backref="user",
    cascade="all, delete-orphan")

    reviews = relationship(              # Relation entre le user et ses review
    "Review",
    back_populates="user",
    cascade="all, delete-orphan")
# --------------------------------------- Définition des attributs de la classe
    def __init__(
        self, first_name, last_name, email, password, is_admin=False
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
        self.password = password

# ---------------------------------------- Représentation visuelle de la classe
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

# ------------------------------------------------------- Gestion du first_name
    @hybrid_property
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

        value = value.strip()
        if not value or not value.strip():
            raise ValueError("first_name is required and cannot be empty")
        if len(value) > 50:
            raise ValueError(
                "first_name is too long, more than 50 characters")
        self._first_name = value

# -------------------------------------------------------- Gestion du last_name
    @hybrid_property
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
        if not isinstance(value, str):
            raise TypeError("last_name must be a string")

        value = value.strip()
        if not value or not value.strip():
            raise ValueError("last_name is required and cannot be empty")
        if len(value) > 50:
            raise ValueError(
                "last_name is too long, more than 50 characters")
        self._last_name = value

# ---------------------------------------------------------- Gestion de l'email
    @hybrid_property
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
        if not isinstance(value, str):
            raise TypeError("email must be a string")

        # Vérifie si la valeur de l'email est vide
        if not value or not value.strip():
            raise ValueError("email is required and cannot be empty")

        # Variable pour cleaner la valeur de l'email
        cleaned_email = value.strip()

        # Vérifie si après le clean de l'email le format est valide
        if not self.email_valid(cleaned_email):
            raise ValueError("Email format is invalid")

        from app.models.user import User as UserModel  # évite circular import

        # Récupère le user par sont email (utile pour search, modif et delete)
        existing_user = UserModel.query.filter_by(email=cleaned_email).first()

        # Vérifie si l'email est déjà utilisé
        if existing_user and existing_user.id != self.id:
            raise ValueError("This email is already used")

        self._email = cleaned_email

    @staticmethod
    def email_valid(email):
        """
        Validate the email format.

        Args:
            email (str): The email string to validate.

        Returns:
            bool: True if the email matches the expected pattern,
            False otherwise.
        """
        # Regex de validation d'email
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Vérifie la syntaxe du mail par rapport à la regex
        match = re.match(pattern, email)

        # Vérifie si il y a match ou pas
        if match is not None:
            return True         # Match OK
        else:
            return False        # Match NOK

# --------------------------------------------------------- Gestion du is_admin
    @hybrid_property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if type(value) is not bool:
            raise ValueError("Is_admin must be a boolean")
        self._is_admin = value

# --------------------------------------------------------- Gestion du password
    @hybrid_property
    def password(self):
        """The password is write-only and cannot be read."""
        raise AttributeError("The password is not accessible in read")

    @password.setter
    def password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self._password_hash = (
            bcrypt
            .generate_password_hash(password)
            .decode('utf-8'))

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self._password_hash, password)

# ----------------------------------------- Transforme un objet en dictionnaire
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
