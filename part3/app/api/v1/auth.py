from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
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

        # Retourne le token
        return {'access_token': access_token}, 200
# --------------------------------------------- Fonction pour vérifier le token
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Récupère le user.id par sont token
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
