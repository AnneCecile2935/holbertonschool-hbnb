from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400


    @api.response(200, 'User successfully found')
    @api.response(404, 'User not found')
    @api.response(500, 'Unexpected server error')
    def get(self): # to do remettre à jour
        try:
            email = request.args.get('email')
            if email:
                user = facade.get_user_by_email(email)
                if not user:
                    return {'error': 'User not found'}, 404
                return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }, 200
            else:
                users = facade.get_all_users()
                return [
                    {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email
                    } for user in users
                ], 200
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}, 500


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated succesfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
    def put(self, user_id):
        try:
            update_data = api.payload
            updated_user = facade.update_user(user_id, update_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200

        except ValueError as e:
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400
