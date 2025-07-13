"""
Amenities API Module

This module defines RESTful API endpoints for managing amenities in
the application.
It leverages Flask-RESTX for API routing, validation, and documentation, and
Flask-JWT-Extended for securing endpoints.

Features:
- Create new amenities (secured endpoint).
- Retrieve a list of all amenities.
- Retrieve details of a specific amenity by ID.
- Update an existing amenity (secured endpoint).

Authentication:
- Endpoints that modify data (POST, PUT) require JWT authentication via the
 @jwt_required decorator.

Endpoints:
- GET    /api/v1/amenities/           : Retrieve all amenities.
- POST   /api/v1/amenities/           : Create a new amenity
(authentication required).
- GET    /api/v1/amenities/<id>       : Retrieve a specific amenity by its ID.
- PUT    /api/v1/amenities/<id>       : Update a specific amenity
(authentication required).

Models:
- amenity_model: Defines the expected schema for amenity data with validation.

Error Handling:
- Consistent HTTP status codes and JSON error messages are returned for
invalid input,
  not found resources, and other errors, facilitated by a custom error
  handler decorator.

Usage:
- Include this namespace in the Flask-RESTX API.
- Ensure JWT authentication is properly configured for secured endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.decorators import handle_errors
from flask_jwt_extended import jwt_required


api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'amenities',                        # Le nom du Namespace
    description='Amenity operations'    # Documentation autogénérée de l'API
)
# ------------------------------------------- modèle de données pour validation
# Sert à valider automatiquement les entrées dans les requêtes

amenity_model = api.model('Amenity', {          # "model" permet de déclarer
    'name': fields.String(                      # "fields.String" = string
        required=True,                          # Champ obligatoire
        description='Name of amenity'           # Description
    )
})


# --------------------------------------- Route POST & GET : /api/v1/amenities/
@api.route('/')                 # Création d'une route
class AmenityList(Resource):    # Récupération des méthodes par Resource
    """
    Resource for listing all amenities and creating a new amenity.

    Methods:
    - GET: Retrieve a list of all amenities.
    - POST: Create a new amenity. Requires a valid JWT token.

    Responses:
    - GET 200: Returns a list of amenities.
    - POST 201: Amenity created successfully.
    - POST 400: Invalid input or amenity name already exists.
    """
    @api.expect(amenity_model, validate=True)      # Vérifie avec amenity_model
    @api.response(201, 'Amenity successfully created')                    # OK
    @api.response(400, 'Invalid input data or name already registered')   # NOK
    @handle_errors
# ---------------------------------- Fonction pour enregister un nouvel amenity
    @jwt_required()
    def post(self):
        """
        Create a new amenity.

        Validates input data and creates a new amenity entry.

        Returns:
            JSON object of the created amenity with its ID and name.
            HTTP 201 status on success.

        Errors:
            HTTP 400 if input data is invalid or the amenity name is already
              registered.
        """
        amenity_data = api.payload                  # Récupère les données
        # Vérifie les données et si OK crée un nouvel amenity
        new_amenity = facade.create_amenity(amenity_data)
        return {                           # Retourne un obj JSON key/value
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201                                                # Création Ok

# --------------------------------------- Route POST & GET : /api/v1/amenities/
    @api.response(200, 'List of amenites retrieved successfully')
# ------------------------------ Fonction pour récupérer la liste des amenities
    def get(self):
        """
        Retrieve all amenities.

        Returns:
            JSON list of amenities, each containing 'id' and 'name'.
            HTTP 200 status.
        """
        amenities = facade.get_all_amenities()       # Récupération de la liste
        amenities_list = []                          # Liste vide
        for amenity in amenities:            # Boucle dans le _storage
            amenities_list.append({          # Ajoute chaque amenity à la liste
                'id': amenity.id,
                'name': amenity.name
            })
        return amenities_list, 200           # Return la liste


# ---------------------------- Route GET & PUT : /api/v1/amenities/<amenity_id>
@api.route('/<amenity_id>')         # Création d'une route
class AmenityResource(Resource):    # Récupération des méthodes par Resource
    """
    Resource for retrieving and updating a specific amenity by ID.

    Methods:
    - GET: Retrieve details of the amenity.
    - PUT: Update the amenity. Requires a valid JWT token.

    Responses:
    - GET 200: Amenity details retrieved successfully.
    - GET 404: Amenity not found.
    - PUT 200: Amenity updated successfully.
    - PUT 400: Invalid input data.
    - PUT 404: Amenity not found.
    """
    @api.response(200, 'Amenity details retrieved successfully')    # OK
    @api.response(404, 'Amenity not found')                         # NOK
# ------------------------------- Fonction pour récupérer un amenity par son id
    def get(self, amenity_id):
        """
        Retrieve an amenity by its ID.

        Args:
            amenity_id (str): ID of the amenity to retrieve.

        Returns:
            JSON object with 'id' and 'name' of the amenity.
            HTTP 200 status if found.

        Errors:
            HTTP 404 if the amenity with the given ID does not exist.
        """
        amenity = facade.get_amenity(amenity_id)   # Récupère l'id de l'amenity
        if not amenity:                            # Si amenity id pas trouvé
            return {'error': 'Amenity not found'}, 404                 # Erreur
        return {                                   # Sinon retourne l'amenity
            'id': amenity.id,
            'name': amenity.name
        }, 200                                     # Récupération OK

# ---------------------------- Route GET & PUT : /api/v1/amenities/<amenity_id>
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @handle_errors
# -------------------------------- Fonction pour modifier un amenity par son id
    @jwt_required()
    def put(self, amenity_id):
        """
        Update an existing amenity by its ID.

        Args:
            amenity_id (str): ID of the amenity to update.

        Validates input data and updates the amenity.

        Returns:
            JSON object with updated amenity details ('id' and 'name').
            HTTP 200 status on success.

        Errors:
            HTTP 404 if amenity is not found.
            HTTP 400 if input data is invalid.
        """
        amenity_data = api.payload             # Récupère nouvelles données
        # Vérifie les nouvelles données et si OK modifie l'amenity
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200                                          # OK
