"""
Admin Module

This module provides API endpoints for administrative operations related
 to user management,
amenities, and places within the application.

It includes:

- Creation and modification of users by administrators.
- Creation and modification of amenities.
- Updating place details with access control (only admins or owners can
update places).
- A decorator to restrict access to admin-only endpoints.
- Input validation using Flask-RESTx models.
- Error handling with custom decorators.

Authentication and authorization are enforced using JWT tokens. Admin
privileges are checked
via the 'is_admin' claim in the JWT identity.

Endpoints:
- POST   /users/             : Create a new user (admin only).
- PUT    /users/<user_id>    : Update user details (admin only).
- POST   /amenities/         : Create a new amenity (admin only).
- PUT    /amenities/<amenity_id> : Update an existing amenity (admin only).
- PUT    /places/<place_id>  : Update a place (admin or owner only).

Models:
- Admin_User: Model for creating a user.
- Admin_UserUpdate: Model for updating a user.
- Admin_Amenity: Model for creating or updating an amenity.
- Admin_PlaceUpdate: Model for updating a place.

Usage:
This module is intended to be included as part of the API blueprint and
should be protected with proper JWT authentication.

"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from functools import wraps
from app.utils.decorators import handle_errors
from werkzeug.security import generate_password_hash

api = Namespace(
    'admin',
    description='Admin operations'
)
# ====================
# Models
# ====================


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
    'is_admin': fields.Boolean(
        required=True,
        description='User is or not admin'
    ),
    'password': fields.String(
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
    'password': fields.String(
        description='User pass_word of new user will be hashed automatically'
    )
})
admin_amenity_model = api.model('Admin_Amenity', {
    'name': fields.String(                      # "fields.String" = string
        required=True,                          # Champ obligatoire
        description='Name of amenity'           # Description
    )
})
admin_place_update_model = api.model('Admin_PlaceUpdate', {
    'title': fields.String(
        description='Title of the place'
    ),
    'description': fields.String(
        description='Description of the place'
    ),
    'price': fields.Float(
        description='Price per night'
    ),
    'latitude': fields.Float(
        description='Latitude coordinate'
    ),
    'longitude': fields.Float(
        description='Longitude coordinate'
    )
})
# ====================
# Utility decorators
# ====================


def admin_only(f):
    """
    Decorator to restrict access to admin users only.

    Requires a valid JWT token and checks the 'is_admin' claim in the
    token identity.
    Returns HTTP 403 Forbidden if the user is not an admin.
    """
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        # remplace fct inter remplece f,
        # accepte tous args pour s'adapter à n'importe quelle fct décorée
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return f(*args, **kwargs)
    # si le admin, on execute fct décorée en passant tous les arg
    return decorated
    # retour de la fonction décorée


# ====================
# Routes
# ====================


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(admin_user_model, validate=True)
    @api.response(201, 'User successfully created')                       # OK
    @api.response(400, 'Invalid input data or email already registered')  # NOK
    @admin_only
    @handle_errors
    def post(self):
        """
        Create a new user.

        This endpoint allows an admin user to create a new user.
        Passwords will be hashed automatically.

        Returns:
            JSON containing the new user's ID and a success message.
        """
        user_data = api.payload
        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User created successfully'}, 201


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(admin_user_update_model, validate=True)
    @api.response(200, 'User modified successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
    @admin_only
    @handle_errors
    def put(self, user_id):
        """
        Update an existing user's information.

        Allows partial or full update of user details by admin.
        Password updates will be hashed automatically.

        Args:
            user_id (str): ID of the user to update.

        Returns:
            JSON containing updated user info.
        """
        updated_user_data = api.payload
        if 'password' in updated_user_data:
            updated_user_data['password'] = generate_password_hash(updated_user_data['password'])
        updated_user = facade.update_user(user_id, updated_user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(admin_amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')                    # OK
    @api.response(400, 'Invalid input data or name already registered')   # NOK
    @admin_only
    @handle_errors
    def post(self):
        """
        Create a new amenity.

        Admins can add new amenities to the system.

        Returns:
            JSON containing the new amenity's ID and name.
        """
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(admin_amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @admin_only
    @handle_errors
    def put(self, amenity_id):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): ID of the amenity to update.

        Returns:
            JSON containing the updated amenity's ID and name.
        """
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(admin_place_update_model, validate=True)
    @api.response(200, 'Place updated succesfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    @handle_errors
    def put(self, place_id):
        """
        Update a place's details.

        Only admins or the owner of the place can perform updates.
        Modification of the 'owner' field is forbidden.

        Args:
            place_id (str): ID of the place to update.

        Returns:
            JSON containing updated place details.
        """
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        update_data = api.payload          # Récupère les nouvelles données
        if 'owner' in update_data:
            return {
                'error': "Modification of 'owner' field is not allowed."
            }, 400

        updated_place = facade.update_place(place_id, update_data)
        return {
            'id': updated_place.id,
            'description': updated_place.description,
            'title': updated_place.title,
            'price': updated_place.price,
        }, 200
