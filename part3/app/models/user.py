"""User model definition with validation and secure password handling."""
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from app.models.base_model import BaseModel
import re                                       # Validation syntaxe de l'email


class User(BaseModel):
    """User model class that stores personal info,
    credentials, and relationships."""
    __tablename__ = 'users'                      # Création de la table 'users'
# ------------------------------------- Création des colonnes de la table users
    _first_name = db.Column(           # Création de la colonne 'first_name'
        db.String(50),                 # Value = String -> 50 char max
        nullable=False)                # Ne peux pas être NULL

    _last_name = db.Column(            # Création de la colonne 'last_name'
        db.String(50),                 # Value = String -> 50 char max
        nullable=False)                # Ne peux pas être NULL

    _email = db.Column(                # Création de la colonne 'email'
        db.String(120),                # Value = String -> 120 char max
        nullable=False,                # Ne peux pas être NULL
        unique=True)                   # Doit être unique

    _password_hash = db.Column(        # Création de la colonne 'password_hash'
        db.String(128),                # Value = String -> 128 char max
        nullable=False)                # Ne peux pas être NULL

    _is_admin = db.Column(              # Création de la colonne 'is_admin'
        db.Boolean,                     # Value = Boolean
        default=False)                  # Ne peux pas être NULL

    places = db.relationship(           # Lien avec Place
        "Place",                        # Nom de la classe liée
        back_populates="owner_rel",      # Nom de la liste dans Place
        cascade="all, delete-orphan")   # Gestion de la récupération et delete

    reviews = db.relationship(          # Lien avec Review
        "Review",                       # Nom de la classe liée
        back_populates="user",          # Nom de la liste dans Review
        cascade="all, delete-orphan")   # Gestion de la récupération et delete

# --------------------------------------- Définition des attributs de la classe
    def __init__(
        self, first_name, last_name, email, password, is_admin=False
    ):
        """Initialize a new User instance with required attributes."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password

# ---------------------------------------- Représentation visuelle de la classe
    def __repr__(self):
        """String representation of the User instance."""
        return (
            f"\nUser = (\n"
            f" id = {self.id},\n"
            f" first_name = {self.first_name},\n"
            f" last_name = {self.last_name},\n"
            f" email = {self.email},\n"
            f" is_admin = {self.is_admin},\n"
            f" created_at = {self.created_at},\n"
            f" updated_at = {self.updated_at},\n"
            f")"
        )

# ------------------------------------------------------- Gestion du first_name
    @hybrid_property
    def first_name(self):
        """User's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """User's first name."""
        # Vérifie que la valeur est une string
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")

        # Nettoyage de la valeur
        value = value.strip()

        # Vérifie que la valeur n'est pas vide
        if not value.strip():
            raise ValueError("first_name is required and cannot be empty")
        # Vérifie que le max de caractère
        if len(value) > 50:
            raise ValueError(
                "first_name is too long, more than 50 characters")

        # Si tout est Ok passe la valeur à l'attribut
        self._first_name = value

# -------------------------------------------------------- Gestion du last_name
    @hybrid_property
    def last_name(self):
        """User's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """User's last name."""
        # Vérifie si la valeur est une string
        if not isinstance(value, str):
            raise TypeError("last_name must be a string")

        # Nettoie la valeur
        value = value.strip()

        # Vérifie si la valeur est vide
        if not value.strip():
            raise ValueError("last_name is required and cannot be empty")
        # Vérifie le maximum de caractères
        if len(value) > 50:
            raise ValueError(
                "last_name is too long, more than 50 characters")

        # Si tout est OK passe la valeur à l'attribut
        self._last_name = value

# ---------------------------------------------------------- Gestion de l'email
    @hybrid_property
    def email(self):
        """User's email address."""
        return self._email

    @email.setter
    def email(self, value):
        """User's email address."""
        # Vérifie que la valeur est une string
        if not isinstance(value, str):
            raise TypeError("email must be a string")

        # Vérifie si la valeur de l'email est vide
        if not value.strip():
            raise ValueError("email is required and cannot be empty")

        # Variable pour cleaner la valeur de l'email
        cleaned_email = value.strip()

        # Vérifie si après le clean de l'email le format est valide
        if not self.is_valid_email(cleaned_email):
            raise ValueError("Email format is invalid")

        # Si tout est OK passe la valeur à l'attribut
        self._email = cleaned_email

    @staticmethod
    def is_valid_email(email):
        """Check if the given email has a valid syntax."""
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
        """User's admin status."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """User's admin status."""
        # Vérifie si la valeur est un booléen
        if type(value) is not bool:
            raise ValueError("Is_admin must be a boolean")

        # Si tout est OK passe la valeur à l'attribut
        self._is_admin = value

# --------------------------------------------------------- Gestion du password
    @hybrid_property
    def password(self):
        """The password is write-only and cannot be read."""
        raise AttributeError("The password is not accessible in read")

    @password.setter
    def password(self, password):
        """Hashes the password before storing it."""
        # Vérifie si la valeur est vide
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")

        from app import bcrypt                              # Import de Bcrypt
        # Génère le hashage du password
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
        """Convert the User instance to a dictionary for serialization."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
