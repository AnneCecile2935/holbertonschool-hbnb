from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace(
    'admin',
    description='Admin operations'
)

admin_user_model = api.model('Admin_User', {
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
    'user_password' : fields.String(
        required=True,
        description='User pass_word of new user will be hashed automatically'
    )
})
admin_user_update_model = api.model('Admin_UserUpdate', {
    'first_name': fields.String(
        description='First name of the user'
    ),
    'last_name': fields.String(
        description='Last name of the user'
    ),
    'email': fields.String(
        description='Email of the user'         # Description
    ),
    'user_password' : fields.String(
        description='User pass_word of new user will be hashed automatically'
    )
})
admin_amenity_model = api.model('Admin_Amenity', {          # "model" permet de déclarer
    'name': fields.String(                      # "fields.String" = string
        required=True,                          # Champ obligatoire
        description='Name of amenity'           # Description
    )
})
admin_place_update_model = api.model('Admin_PlaceUpdate', {    # "model" permet de déclarer
    'title': fields.String(                         # "fields.String" = string
        description='Title of the place'            # Description
    ),
    'description': fields.String(                   # "fields.String" = string
        description='Description of the place'      # Description
    ),
    'price': fields.Float(                          # "fields.Float" = Float
        description='Price per night'               # Description
    ),
    'latitude': fields.Float(                       # "fields.Float" = Float
        description='Latitude coordinate'           # Description
    ),
    'longitude': fields.Float(                      # "fields.Float" = Float
        description='Longitude coordinate'          # Description
    )
})
@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(admin_user_model, validate=True)
    @api.response(201, 'User successfully created')                       # OK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()        # Récupère le token du user courant
            if not current_user.get('is_admin'):     # Vérifie si le user courant est un admin
                return {'error': 'Admin privileges required'}, 403  # Si il ne l'est pas = Erreur

            user_data = api.payload                  # Récupère les données passées par le user
            # Vérifie les données et si ok crée un nouvel user
            new_user = facade.create_user(user_data)
            return {                           # Retourne un obj JSON key/value
                'id': new_user.id,
                'message': 'User created successfully'
            }, 201                                                # Création Ok
        except (ValueError, TypeError) as e:   # Utilise les méthodes de classe
            return {'error': str(e)}, 400     # Return obj error et code status


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(admin_user_update_model, validate=True)            # Vérifie avec user_model
    @api.response(200, 'User modified successfully')                      # OK
    @api.response(404, 'User not found')                                  # NOK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
    @jwt_required()
    def put(self, user_id):
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            updated_user_data = api.payload
            # Vérifie les nouvelles données et si OK modifie le user
            updated_user = facade.update_user(user_id, updated_user_data)
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

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(admin_amenity_model, validate=True)      # Vérifie avec amenity_model
    @api.response(201, 'Amenity successfully created')                    # OK
    @api.response(400, 'Invalid input data or name already registered')   # NOK
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            amenity_data = api.payload                  # Récupère les données
            # Vérifie les données et si OK crée un nouvel amenity
            new_amenity = facade.create_amenity(amenity_data)
            return {                           # Retourne un obj JSON key/value
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201                                                # Création Ok
        except (TypeError, ValueError) as e:  # Utilise les méthodes de classe
            return {'error': str(e)}, 400     # Return obj error et code status

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(admin_amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403
            amenity_data = api.payload             # Récupère nouvelles données
            # Vérifie les nouvelles données et si OK modifie l'amenity
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200                                          # OK
        except ValueError as e:
            # Si le message d'erreur contient 'not found'
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404               # Return 404
            return {'error': str(e)}, 400

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(admin_place_update_model, validate=True)
    @api.response(200, 'Place updated succesfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        try:
            current_user = get_jwt_identity()

            # Set is_admin default to False if not exists
            is_admin = current_user.get('is_admin', False)
            user_id = current_user.get('id')

            place = facade.get_place(place_id)
            if not is_admin and place.owner_id != user_id:
                return {'error': 'Unauthorized action'}, 403

            update_data = api.payload          # Récupère les nouvelles données
            # Vérification que un champ owner est été remplis
            if 'owner' in update_data:
                return {
                    'error': "Modification of 'owner' field is not allowed."
                }, 400
            # Vérifie les nouvelles données et si OK modifie la place
            updated_place = facade.update_place(place_id, update_data)
            return {
                'id': updated_place.id,
                'description': updated_place.description,
                'title': updated_place.title,
                'price': updated_place.price,
            }, 200
        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}, 400
