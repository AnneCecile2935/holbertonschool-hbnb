"""Defines 'place_amenity' table for the many-to-many
relation between Place and Amenity."""
from app.extensions import db

# ----------------------------- Création des colonnes de la table place_amenity
place_amenity = db.Table(                # Table liaison entre place et amenity
    'place_amenity',                     # Nom de la table
    db.Column('place_id',                # Définition de la colonne et son nom
              db.String,                        # Type String
              db.ForeignKey('places.id'),       # La donnée = id
              primary_key=True),                # Lien avec la table place
    db.Column('amenity_id',              # Définition de la colonne et son nom
              db.String,                        # Type String
              db.ForeignKey('amenities.id'),    # La donnée = id
              primary_key=True)                 # Lien avec la table amenity
)
