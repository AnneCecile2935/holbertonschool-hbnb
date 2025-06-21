from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or name already registered')
    @api.response(500, 'Internal server error')
    def post(self):
        """Register a new amenity"""
        try:

            amenity_data = api.payload

            name = amenity_data.get('name')

            if name is None:
                return {'error': 'Name is required'}, 400

            try:
                existing_amenity = facade.get_amenity_by_name(name)
                if existing_amenity:
                    return {'error': 'Name already registered'}, 400

                # On laisse la classe Amenity gérer le strip() et les validations
                new_amenity = facade.create_amenity({'name': name})
            except (TypeError, ValueError) as e:
                return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}, 500

        return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""

        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""

        try:
            update_data = api.payload

            # On délègue la validation à la façade et à la classe Amenity
            updated_amenity = facade.update_amenity(amenity_id, update_data)

            if updated_amenity is None:
                return {'error': 'Amenity not found'}, 404

            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
            }, 200

        except ValueError as e:
            # Gestion des erreurs liées à la validation (ex: nom vide, déjà utilisé)
            return {'error': str(e)}, 400

        except Exception as e:
            # Toute autre erreur inattendue
            return {'error': f'Internal server error: {str(e)}'}, 500
