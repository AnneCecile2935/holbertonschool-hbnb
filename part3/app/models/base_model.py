"""Abstract base model with id, timestamps, and basic methods."""
from app.extensions import db
from datetime import datetime
import uuid
class BaseModel(db.Model):
    """Base model with common fields and methods (abstract)."""
    __abstract__ = True              # Pas de table crée mais colonnes héritées
# ------------------------------------------------------- Création des colonnes
    id = db.Column(                             # Création de la colonne 'id'
        db.String(36),                          # Value = String -> 36 char max
        primary_key=True,                       # Identifiant unique
        default=lambda: str(uuid.uuid4()))      # Génération aléatoire de l'id

    created_at = db.Column(            # Création de la colonne 'created_at'
        db.DateTime,                   # Value = DateTime
        default=datetime.now,          # Value par défaut = date/heure actuelle
        nullable=False)                # Ne peux pas être NULL

    updated_at = db.Column(           # Création de la colonne 'updated_at'
        db.DateTime,                  # Value = DateTime
        default=datetime.now,         # Value par défaut = date/heure actuelle
        onupdate=datetime.now,        # Value mise à jour = date/heure actuelle
        nullable=False)               # Ne peux pas être NULL

# --------------------------------------- Définition des attributs de la classe
    def __init__(self):
        """Initialize model with unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

# ---------------------------------------------------------- Méthode de classe
    # Mise à jour et sauvegarde des champs de Base_model
    def update(self, data):
        """Update attributes from a dictionary and commit the changes."""
        # Boucle sur chaque clé et valeur dans le dictionnaire data
        for key, value in data.items():
            # Vérifie si la key/value existe dans la BDD
            if not hasattr(self, key):
                raise AttributeError(
                    f"{key} is not a valid attribute of {type(self).__name__}")
            setattr(self, key, value)           # Modifie la mémoire

        self.updated_at = datetime.now()        # Récupère la datetime actuelle
        db.session.commit()                     # Envoie à la BDD
