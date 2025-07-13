"""
Places API module.

This module defines RESTful API endpoints to manage places using Flask-RESTX.
It supports creating, retrieving, updating, and listing places.

Endpoints:
- GET, POST /api/v1/places/: List all places or create a new place.
- GET, PUT /api/v1/places/<place_id>: Retrieve or update a specific place.

Models:
- place_model: Schema for place creation with validation.
- place_update_model: Schema for place update with validation.

Error handling returns appropriate HTTP status codes and messages.
"""


from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.users import user_place_model
from app.utils.decorators import handle_errors

api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'places',                           # Le nom du Namespace
    description='Place operations'      # Documentation autogénérée de l'API
)
# ----------------------------- modèle de données pour validation à la création
# Sert à valider automatiquement les entrées dans les requêtes

place_model = api.model('Place', {                 # "model" permet de déclarer
    'title': fields.String(                         # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='Title of the place'            # Description
    ),
    'description': fields.String(                   # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Description of the place'      # Description
    ),
    'price': fields.Float(                          # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Price per night'               # Description
    ),
    'latitude': fields.Float(                       # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Latitude coordinate'           # Description
    ),
    'longitude': fields.Float(                      # "fields.Float" = Float
        required=True,                              # Champ obligatoire
        description='Longitude coordinate'          # Description
    ),
    'owner': fields.String(                         # "fields.String" = string
        required=True,                              # Champ obligatoire
        description='Owner user ID'                 # Description
    )
})
# ------------------------- modèle de données pour validation à la modification
place_update_model = api.model('PlaceUpdate', {    # "model" permet de déclarer
    'title': fields.String(                         # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Title of the place'            # Description
    ),
    'description': fields.String(                   # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Description of the place'      # Description
    ),
    'price': fields.Float(                          # "fields.String" = string
        required=False,                             # Champ non obligatoire
        description='Price per night'               # Description
    )
})
# ------------------------------------------------ modèle de données détaillées
place_detail_model = api.model('PlaceDetailModel', {
    'id': fields.String(),                          # "fields.String" = string
    'title': fields.String(),                       # "fields.String" = string
    'description': fields.String(),                 # "fields.String" = string
    'price': fields.Float(),                        # "fields.Float" = Float
    'latitude': fields.Float(),                     # "fields.Float" = Float
    'longitude': fields.Float(),                    # "fields.Float" = Float
    'owner': fields.Nested(user_place_model),       # "fields.Nested" = Dict
    # fields.List = une liste qui contient des sous dictionnaires : Nested
    'amenities': fields.List(fields.Nested(api.model('AmenityMiniModel', {
        'id': fields.String(),                      # "fields.String" = string
        'name': fields.String()                     # "fields.String" = string
    }))),
    # fields.List = une liste qui contient des sous dictionnaires : Nested
    'reviews': fields.List(fields.Nested(api.model('ReviewMiniModel', {
        'id': fields.String(),                      # "fields.String" = string
        'rating': fields.Integer(),                # "fields.Integer" = Integer
        'comment': fields.String()                  # "fields.String" = string
    })))
})


# ------------------------------------------ Route POST & GET : /api/v1/places/
@api.route('/')                        # Création d'une route
class PlaceList(Resource):             # Récupération des méthodes par Resource
    """Resource for creating a new place and listing all places."""
    @api.expect(place_model, validate=True)          # Vérifie avec place_model
    @api.response(201, 'Place successfully created')                    # OK
    @api.response(400, 'Bad request')                                   # NOK
# --------------------------------- Fonction pour enregister une nouvelle place
    @handle_errors
    @jwt_required()
    def post(self):
        """
        Register a new place.

        Expects JSON payload matching place_model.
        Validates owner existence and ownership.

        Returns:
            JSON with new place details and HTTP 201 on success,
            or error message with HTTP 400/403 on failure.
        """
        current_user = get_jwt_identity()
        place_data = api.payload
        if "owner" not in place_data:
            return {'error': "Missing 'owner' field"}, 400
        owner_id = place_data.get("owner")
        owner = facade.get_user(owner_id)
        if not owner:
            return {'error': 'Owner user not found'}, 400
        elif owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': new_place.owner
            }, 201

# ------------------------------------------ Route POST & GET : /api/v1/places/
    @api.response(200, 'Places found', place_detail_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve all places.

        Returns:
            JSON list of places with HTTP 200.
        """
        places = facade.get_all_places()       # Récupération de la liste
        places_list = []                       # Liste vide

        for place in places:
            # Récupérer le owner
            owner = facade.get_user(place.owner)

            # Construction du dictionnaire owner
            owner_data = {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None

            # Construction de la liste des amenities
            amenities = []
            for amenity in place.amenities:
                amenity_data = {}
                amenity_data["id"] = amenity.id
                amenity_data["name"] = amenity.name
                amenities.append(amenity_data)

            # Construction de la liste des reviews
            reviews = []
            for review in place.reviews:
                review_data = {}
                review_data["id"] = review.id
                review_data["rating"] = review.rating
                review_data["text"] = review.text
                reviews.append(review_data)

            # Construction de la place complète
            places_list.append({
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": owner_data,
                "amenities": amenities,
                "reviews": reviews
            })
        return places_list, 200


# --------------------------------- Route GET & PUT : /api/v1/places/<place_id>
@api.route('/<place_id>')              # Création d'une route
class PlaceResource(Resource):         # Récupération des méthodes par Resource
    """Resource for retrieving and updating a specific place by ID."""
    @api.response(200, 'Place found', place_detail_model)
    @api.response(200, 'Place details retrieved successfully')  # OK
    @api.response(404, 'Place not found')                       # NOK
    @api.response(404, 'Owner not found')                       # NOK
# -------------------------------- Fonction pour récupérer une place par son id
    def get(self, place_id):
        """
        Retrieve place details by ID.

        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            JSON with place and owner details and HTTP 200 on success,
            or error message with HTTP 404 if not found.
        """
        place = facade.get_place(place_id)        # Récupère l'id de la place
        if not place:                             # Si pas trouvé = Erreur
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner)      # Récupère le owner
        if not owner:                             # Si il n'existe pas = Erreur
            return {'error': 'Owner not found'}, 404
        amenities = []
        for amenity in place.amenities:
            amenity_data = {}
            amenity_data["id"] = amenity.id
            amenity_data["name"] = amenity.name
            amenities.append(amenity_data)
        reviews = []
        for review in place.reviews:
            review_data = {}
            review_data["id"] = review.id
            review_data["rating"] = review.rating
            review_data["comment"] = review.text
            reviews.append(review_data)

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
            'amenities': amenities,
            'reviews': reviews
        }, 200                                          # Récupération OK

# --------------------------------- Route GET & PUT : /api/v1/places/<place_id>
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated succesfully')
    @api.response(404, 'Place not found')
# --------------------------------- Fonction pour modifier une place par son id
    @handle_errors
    @jwt_required()
    def put(self, place_id):
        """
        Update a place by its ID.

        Args:
            place_id (str): The ID of the place to update.

        Expects JSON payload matching place_update_model.

        Restrictions:
            - Updating the 'owner' field is not allowed.

        Returns:
            JSON with updated place details and HTTP 200 on success,
            or error message with HTTP 400/403/404 on failure.
        """
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)  # Récupère la place par sont id
        if str(place.owner) != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        elif not place:              # Si la place n'est pas trouvée = Erreur
            return {'error': 'Place not found'}, 404
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
