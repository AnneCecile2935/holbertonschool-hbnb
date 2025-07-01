from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig #import propre
from flask_jwt_extended import JWTManager
#-------------------------------------------------------------- Import namespace
from flask_jwt_extended import JWTManager                   #extension génération de token
from app.api.v1.users import api as users_ns                # users
from app.api.v1.amenities import api as amenities_ns        # amenities
from app.api.v1.places import api as places_ns              # places
from app.api.v1.reviews import api as reviews_ns            # amenities
from app.api.v1.auth import api as auth_ns
#------------------------------------------------------------------- App et Docu
jwt = JWTManager()
bcrypt = Bcrypt() #rend accessible bcrypt depuis les autres modules
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Ajoutez un JWT avec **Bearer <token>**'
    }
}
# Fonction qui retourne l'application complète et la documentation Swagger
def create_app(config_class="config.DevelopmentConfig"): #devconfig sera automatiquement appliqué
    app = Flask(__name__)   # Création application Flask
    app.config.from_object(config_class) # applique la configuration
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(              # Infos pour la documentation Swagger
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations=authorizations,
        security='Bearer Auth'
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
    # Ajout du namespace de auth à l'API principale
    api.add_namespace(auth_ns, path="/api/v1")



    return app
