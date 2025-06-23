"""
Users API module.

This module provides endpoints to manage user entities.
It supports creating new users, retrieving all users,
getting a user by ID, and updating user information.

Endpoints:
- /api/v1/users/ [GET, POST]: List all users or create a new user.
- /api/v1/users/<user_id> [GET, PUT]: Retrieve or update a user by ID.

Models:
- user_model: Schema for user creation and validation.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'users',      # Le nom du Namespace
    description='User operations'  # Documentation autogénérée de l'API
)

# ------------------------------------------- modèle de données pour validation
# Sert à valider automatiquement les entrées dans les requêtes
# Déclarer les champs obligatoires, tous de type string

user_model = api.model('User', {                # "model" permet de déclarer
    'first_name': fields.String(                # "fields.String" = string
        required=True,                          # Champ obligatoire
        description='First name of the user'    # Description
    ),
    'last_name': fields.String(
        required=True,                          # Champ obligatoire
        description='Last name of the user'     # Description
    ),
    'email': fields.String(
        required=True,                          # Champ obligatoire
        description='Email of the user'         # Description
    )
})
user_place_model = api.model('UserPlaceModel', {                 # "model" permet de déclarer
    'id': fields.String(                         # Ajout de l'ID
        required=True,                           # Champ obligatoire
        description='Unique identifier of the user'  # Description
    ),
    'first_name': fields.String(                 # "fields.String" = string
        required=True,                           # Champ obligatoire
        description='First name of the user'     # Description
    ),
    'last_name': fields.String(
        required=True,                           # Champ obligatoire
        description='Last name of the user'      # Description
    ),
    'email': fields.String(
        required=True,                           # Champ obligatoire
        description='Email of the user'          # Description
    )
})


# ------------------------------------------- Route POST & GET : /api/v1/users/
@api.route('/')                 # Création d'une route
class UserList(Resource):       # "Resource" = methodes requête (POST, GET, ..)
    @api.expect(user_model, validate=True)            # Vérifie avec user_model
    @api.response(201, 'User successfully created')                       # OK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
# ------------------------------------ Fonction pour enregister un nouveau user
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload    # Récup les datas envoyées par le client
            # Vérifie les données et si ok crée un nouvel user
            new_user = facade.create_user(user_data)
            return {                           # Retourne un obj JSON key/value
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201                                                # Création Ok
        except (ValueError, TypeError) as e:   # Utilise les méthodes de classe
            return {'error': str(e)}, 400     # Return obj error et code status

# ------------------------------------------ Route POST & GET : /api/v1/users/
    @api.response(200, 'List of users retrieved successfully')
# ---------------------------------- Fonction pour récupérer la liste des users
    def get(self):
        """Get all users"""
        users = facade.get_all_users()    # Récupère les users dans le _storage
        users_list = []                   # Crée une liste de vide
        for user in users:                # Boucle dans le _storage
            users_list.append({           # Ajoute chaque user à la liste
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })

        return users_list, 200            # Return la liste


# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
@api.route('/<user_id>')        # Création d'une route
class UserResource(Resource):   # Récupération des méthodes par Resource
    @api.response(200, 'User details retrieved successfully')   # OK
    @api.response(404, 'User not found')                        # NOK
# ---------------------------------- Fonction pour récupérer un user par son id
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)           # Récupère l'id par la façade
        if not user:                                    # Si user id pas trouvé
            return {'error': 'User not found'}, 404     # Erreur
        return {                                        # Sinon return le user
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200                                          # Récupération OK

# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
    @api.expect(user_model, validate=True)            # Vérifie avec user_model
    @api.response(200, 'User modified successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
# ----------------------------------- Fonction pour modifier un user par son id
    def put(self, user_id):
        """Put user details by ID"""
        try:
            update_data = api.payload              # Récupère nouvelles données
            # Vérifie les nouvelles données et si OK modifie le user
            updated_user = facade.update_user(user_id, update_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200                                            # Modification OK
        except ValueError as e:
            # Si le message d'erreur contient 'not found'
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404                # Return 404
            return {'error': str(e)}, 400                    # Sinon return 400
