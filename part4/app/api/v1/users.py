"""
Users API module.

This module defines RESTful endpoints for managing users in the system.
It allows creating new users, retrieving all users, fetching a single
user by ID, and updating user information.

Endpoints:
- /api/v1/users/ [GET, POST]: List all users or create a new user.
- /api/v1/users/<user_id> [GET, PUT]: Retrieve or update a user by ID.

Models:
- user_model: Request schema for creating a new user.
- user_place_model: Response schema for listing users (simplified version).
- user_update_model: Request schema for updating user information.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.utils.decorators import handle_errors

api = Namespace(
    'users',
    description='User operations'
)

# ------------------------------------------- modèle de données pour validation

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
    'is_admin': fields.Boolean(
        required=True,
        description='User is or not admin'
    ),
    'password': fields.String(
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
    @handle_errors
# ------------------------------------ Fonction pour enregister un nouveau user
    def post(self):
        """
        Create a new user.

        Validates the request body using `user_model` and creates a new user.
        Returns the ID of the created user.
        """
        user_data = api.payload    # Récup les datas envoyées par le client
        new_user = facade.create_user(user_data)
        return {                           # Retourne un obj JSON key/value
            'id': new_user.id,
            'message': 'User created succesfully'
            }, 201                                                # Création Ok

# ------------------------------------------ Route POST & GET : /api/v1/users/
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve all users.

        Returns a list of all users in the system.
        """
        users = facade.get_all_users()    # Récupère les users dans le _storage
        users_list = [user.to_dict() for user in users]
        return users_list, 200        # Retourne la liste avec code 200


# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
@api.route('/<user_id>')        # Création d'une route
class UserResource(Resource):   # Récupération des méthodes par Resource
    """Handles operations on a single user identified by user_id (GET, PUT)."""
    @api.response(200, 'User details retrieved successfully')   # OK
    @api.response(404, 'User not found')                        # NOK
# ---------------------------------- Fonction pour récupérer un user par son id
    def get(self, user_id):
        """
        Retrieve a user by ID.

        Returns user details if the user exists, or a 404 error if not found.
        """
        user = facade.get_user(user_id)           # Récupère l'id par la façade
        if not user:                                    # Si user id pas trouvé
            return {'error': 'User not found'}, 404     # Erreur
        return user.to_dict(), 200                      # Sinon return le user

# ----------------------------------- Route GET & PUT : /api/v1/users/<user_id>
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User modified successfully')                      # OK
    @api.response(404, 'User not found')                                  # NOK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
    @api.response(403, 'Unauthorized action')                             # NOK
    @handle_errors
    @jwt_required()
    def put(self, user_id):
        """
        Update a user's information by ID.

        Only the authenticated user can update their own profile.
        Accepts partial updates of first name, last name, or email.
        """
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
