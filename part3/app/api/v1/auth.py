"""
Authentication API Module

This module defines RESTful API endpoints for user authentication and
token management.
It uses Flask-RESTX for API routing and documentation, and Flask-JWT-Extended
for JWT-based authentication and authorization.

Features:
- User login to obtain access and refresh JWT tokens.
- Protected endpoint accessible only with a valid access token.
- Token refresh endpoint to get a new access token using a refresh token.

Endpoints:
- POST   /api/v1/auth/login       : Authenticate user and get JWT tokens.
- GET    /api/v1/auth/protected   : Access a protected resource
(requires access token).
- POST   /api/v1/auth/refresh     : Refresh access token
(requires refresh token).

Data Validation:
- Input data for login is validated against the login_model schema,
which requires
  a valid 'email' and 'password'.

Error Handling:
- Invalid login credentials return a 401 Unauthorized response.
- Protected and refresh endpoints require valid JWT tokens.

Usage:
- Register this namespace with your Flask-RESTX API instance.
- Configure Flask-JWT-Extended with appropriate secret keys and settings.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_refresh_token
)
from app.services import facade

api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'auth',                                            # Le nom du Namespace
    description='Authentication operations'            # Documentation de l'API
)

# ------------------------------------------- modèle de données pour validation
login_model = api.model('Login', {                 # "model" permet de déclarer
    'email': fields.String(                         # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='User email'                    # Description
    ),
    'password': fields.String(                      # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='User password'                 # Description
    )
})


# -------------------------------------------- Route POST & GET : /api/v1/auth/
@api.route('/login')
# ------------------------------------------------ Fonction pour créer un token
class Login(Resource):
    """
    Resource for user login and JWT token creation.
    """
    @api.expect(login_model, validate=True)
    def post(self):
        """
        Authenticate user and return access and refresh JWT tokens.

        Expects JSON payload with 'email' and 'password'.

        Returns:
            JSON containing 'access_token' and 'refresh_token' with HTTP
            200 on success.

        Errors:
            HTTP 401 if credentials are invalid.
        """
        credentials = api.payload     # Récupère les données (email + password)
        # Recherche et récupère le user par sont email
        user = facade.get_user_by_email(credentials['email'])

        # Si je user n'existe pas ou que son password est NOK
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401               # Erreur

        # Sinon création d'un token lié par l'user.id
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })
        refresh_token = create_refresh_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        # Retourne le token
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


# --------------------------------------------- Fonction pour vérifier le token
@api.route('/protected')
class ProtectedResource(Resource):
    """
    Resource representing a protected endpoint.

    Requires a valid access JWT token to access.
    """
    @jwt_required()
    def get(self):
        """
        Access a protected resource.

        Returns:
            JSON message greeting the authenticated user by ID with HTTP 200.

        Errors:
            HTTP 401 if access token is missing or invalid.
        """
        # Récupère le user.id par sont token
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200


@api.route('/refresh')
class TokenRefresh(Resource):
    """
    Resource for refreshing an access JWT token using a refresh token.
    """
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh the access token.

        Requires a valid refresh JWT token.

        Returns:
            JSON containing the new 'access_token' with HTTP 200.

        Errors:
            HTTP 401 if refresh token is missing or invalid.
        """
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token': new_access_token}, 200
