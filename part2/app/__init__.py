from flask import Flask
from flask_restx import Api
#-------------------------------------------------------------- Import namespace

from app.api.v1.users import api as users_ns                # users
from app.api.v1.amenities import api as amenities_ns        # amenities
from app.api.v1.places import api as places_ns              # places
from app.api.v1.reviews import api as reviews_ns            # amenities
#------------------------------------------------------------------- App et Docu

# Fonction qui retourne l'application complète et la documentation Swagger
def create_app():
    app = Flask(__name__)   # Création application Flask
    api = Api(              # Infos pour la documentation Swagger
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )
#------------------------------------------------------------------- App et Docu

    # Ajout du namespace de l'utilisateur à l'API principale
    api.add_namespace(users_ns, path='/api/v1/users')
    # Ajout du namespace de amenity à l'API principale
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Ajout du namespace de place à l'API principale
    api.add_namespace(places_ns, path='/api/v1/places')
    # Ajout du namespace de review à l'API principale
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
