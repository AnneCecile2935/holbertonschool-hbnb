from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner': fields.String(required=True, description='Owner user ID')
})
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude coordinate'),
    'longitude': fields.Float(required=False, description='Longitude coordinate')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data or missing required field')
    @api.response(404, 'User not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        #recup données dans le dict en Json

        owner_id = place_data.get("owner")
        #extrait id owner depuis les données
        if not owner_id:
            return {'error': "Missing 'owner' field (must contain owner user ID)"}, 400

        # appel façade pur récup le owner
        owner = facade.get_user(owner_id)
        if not owner:
            return {'error': 'Owner user not found'}, 404

        try:
            # créer place via create place de la façade
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': new_place.id,
            'title' : new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': new_place.owner
            }, 201

    def get(self):
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title' : place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': place.owner,
            }
        for place in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(404, 'Owner not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner)
        if not owner:
            return {'error': 'Owner not found'}, 404
        return {
            'id': place.id,
            'title' : place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
            }
        }, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated succesfully')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def put(self, place_id):
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            update_data = api.payload

            if 'owner' in update_data:
                return {'error': "Modification of 'owner' field is not allowed."}, 400

            updated_place = facade.update_place(place_id, update_data)
            update_owner = facade.get_user(updated_place.owner)
            return {
                'id': updated_place.id,
                'description': updated_place.description,
                'title' : place.title,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
            }, 200
        #to do : est-ce qu'on donne la possibilité de mettre à jour le owner?
        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': f"Internal server error: {str(e)}"}, 500
