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
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    ),
    'is_admin':fields.Boolean(
        required=True,
        description='User is or not admin'
    ),
    'password' : fields.String(
        required=True,
        description='User pass_word of new user will be hashed automatically'
    )
})
user_place_model = api.model('UserPlaceModel', {   # "model" permet de déclarer
    'id': fields.String(                         # "fields.String" = string
        required=True,                           # Champ obligatoire
        description='Unique identifier of the user'  # Description
    ),
    'first_name': fields.String(                 # "fields.String" = string
        required=True,                           # Champ obligatoire
        description='First name of the user'     # Description
    ),
    'last_name': fields.String(                  # "fields.String" = string
        required=True,                           # Champ obligatoire
        description='Last name of the user'      # Description
    ),
    'email': fields.String(                      # "fields.String" = string
        required=True,                           # Champ obligatoire
        description='Email of the user'          # Description
    )
})
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(
        required=False,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=False,
        description='Last name of the user'
    ),
    'email': fields.String(                      # "fields.String" = string
        required=False,                           # Champ non obligatoire
        description='Email of the user'          # Description
    )
})

# ------------------------------------------- Route POST & GET : /api/v1/users/
@api.route('/')                 # Création d'une route
class UserList(Resource):       # "Resource" = methodes requête (POST, GET, ..)
    """Resource to create a new user and retrieve all users."""
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
                'message': 'User created succesfully'
            }, 201                                                # Création Ok
        except (ValueError, TypeError) as e:   # Utilise les méthodes de classe
            return {'error': str(e)}, 400     # Return obj error et code status

# ------------------------------------------ Route POST & GET : /api/v1/users/
    @api.response(200, 'List of users retrieved successfully')
# ---------------------------------- Fonction pour récupérer la liste des users
    def get(self):
        """Get all users"""
        users = facade.get_all_users()    # Récupère les users dans le _storage
        users_list = []                         # Initialise une liste vide

        for user in users:                      # Parcourt chaque user
            user_dict = user.to_dict()          # Transforme en dictionnaire
            users_list.append(user_dict)        # Ajoute à la liste

        return users_list, 200                # Retourne la liste avec code 200

# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
@api.route('/<user_id>')        # Création d'une route
class UserResource(Resource):   # Récupération des méthodes par Resource
    """Resource for retrieving and updating, a user by its ID."""
    @api.response(200, 'User details retrieved successfully')   # OK
    @api.response(404, 'User not found')                        # NOK
# ---------------------------------- Fonction pour récupérer un user par son id
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)           # Récupère l'id par la façade
        if not user:                                    # Si user id pas trouvé
            return {'error': 'User not found'}, 404     # Erreur
        return user.to_dict(), 200                      # Sinon return le user
                                                        # Récupération OK

# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
    @api.expect(user_update_model, validate=True)            # Vérifie avec user_model
    @api.response(200, 'User modified successfully')                      # OK
    @api.response(404, 'User not found')                                  # NOK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
# ----------------------------------- Fonction pour modifier un user par son id
    @jwt_required()
    def put(self, user_id):
        """Put user details by ID"""
        try:
            current_user = get_jwt_identity()
            update_data = api.payload              # Récupère nouvelles données
            if user_id != current_user['id']:
                return {'error': 'Unauthorized action'}, 403
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
