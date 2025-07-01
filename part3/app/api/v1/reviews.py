"""
Reviews API module.

This module provides endpoints for managing reviews associated with places.
It supports creating, retrieving, updating, and deleting reviews,
as well as fetching all reviews for a specific place.

Endpoints:
- /api/v1/reviews/ [GET, POST]: List all reviews or create a new one.
- /api/v1/reviews/<review_id> [GET, PUT, DELETE]:
Retrieve, update, or delete a specific review.
- /api/v1/reviews/places/<place_id>/reviews [GET]:
Get all reviews for a given place.

Models:
- review_model: Schema for review creation and validation.
- review_update_model: Schema for review updates.
- place_model: Schema for places including nested owner, amenities, and reviews
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.api.v1.users import user_model
from app.api.v1.amenities import amenity_model
from flask import request

api = Namespace(  # Namespace permet de regrouper les routes pr une même entité
    'reviews',    # Le nom du Namespace
    description='Review operations'     # Documentation autogénérée de l'API
)

# ------------------------------------------- modèle de données pour validation
# Sert à valider automatiquement les entrées dans les requêtes
# Déclarer les champs obligatoires

review_model = api.model('Review', {               # "model" permet de déclarer
        'place_id': fields.String(                 # "fields.String" = string
            required=True,                         # Champ obligatoire
            description='ID of the place the review is about'   # Description
        ),
        'user_id': fields.String(                  # "fields.String" = string
            required=True,                         # Champ obligatoire
            description='ID of the user who made the review'    # Description
        ),
        'text': fields.String(                     # "fields.String" = string
            required=True,                         # Champ obligatoire
            description='The content of the review'             # Description
        ),
        'rating': fields.Integer(                  # "fields.Integer" = Integer
            required=True,                         # Champ obligatoire
            description='Rating between 1 and 5'                # Description
        )
})
# ----------------------------------------- modèle de données pour modification
review_update_model = api.model('ReviewUpdate', {
        'text': fields.String(                     # "fields.String" = string
            required=True,                         # Champ obligatoire
            description='The content of the review'             # Description
        ),
        'rating': fields.Integer(                  # "fields.Integer" = Integer
            required=True,                         # Champ obligatoire
            description='Rating between 1 and 5'                # Description
        )
})
# ------------------------------------ modèle de données pour renvoyer la place
review_place_model = api.model('ReviewPlacemodel', {
        'title': fields.String(                     # "fields.String" = string
            required=True,                          # Champ obligatoire
            description='Title of the place'        # Description
        ),
        'description': fields.String(               # "fields.String" = string
            description='Description of the place'  # Description
        ),
        'price': fields.Float(                      # "fields.Float" = Float
            required=True,                          # Champ obligatoire
            description='Price per night'           # Description
        ),
        'latitude': fields.Float(                   # "fields.Float" = Float
            required=True,                          # Champ obligatoire
            description='Latitude of the place'     # Description
        ),
        'longitude': fields.Float(                  # "fields.Float" = Float
            required=True,                          # Champ obligatoire
            description='Longitude of the place'    # Description
        ),
        'owner_id': fields.String(                  # "fields.String" = string
            required=True,                          # Champ obligatoire
            description='ID of the owner'           # Description
        ),
        'owner': fields.Nested(                     # "fields.Nested" = Dict
            user_model,                             # modèle = user_model
            description='Owner of the place'        # Description
        ),
        'amenities': fields.List(                   # "fields.List" = Liste
            fields.Nested(amenity_model),           # "fields.Nested" = Dict
            description='List of amenities'         # Description
        ),
        'reviews': fields.List(                     # "fields.List" = Liste
            fields.Nested(review_model),            # "fields.Nested" = Dict
            description='List of reviews'           # Description
        )
})


# ----------------------------------------- Route POST & GET : /api/v1/reviews/
@api.route('/')                 # Création d'une route
class ReviewList(Resource):     # "Resource" = methodes requête (POST, GET, ..)
    """Resource to create a new review and retrieve all reviews."""
    @api.expect(review_model, validate=True)        # Vérifie avec review_model
    @api.response(201, 'Review successfully created')               # OK
    @api.response(400, 'Invalid input data')                        # NOK
    @api.response(400, 'User or Place not found')                   # NOK
# ---------------------------------- Fonction pour enregister un nouveau review
    def post(self):
        """
        Register a new review.

        Expects JSON payload matching review_model.
        Validates referenced place and user existence.

        Returns:
            dict: Created review data with HTTP 201 on success,
                  or error message with HTTP 400 or 404 on failure.
        """
        review_data = api.payload      # Récup les datas envoyées par le client
        try:
            # Vérifie les données et si OK crée un nouveau review
            new_review = facade.create_review(review_data)
            return {                           # Retourne un obj JSON key/value
                'id': new_review.id,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id,
                'text': new_review.text,
                'rating': new_review.rating
            }, 201                              # Création OK

        except (ValueError, TypeError) as e:   # Utilise les methodes de classe
            error_msg = str(e).lower()
            if "place not found" in error_msg or "user not found" in error_msg:
                return {'error': str(e)}, 400
            return {'error': str(e)}, 400

# ----------------------------------------- Route POST & GET : /api/v1/reviews/
    @api.response(200, 'List of reviews retrieved successfully')
# -------------------------------- Fonction pour récupérer la liste des reviews
    def get(self):
        """
        Retrieve a list of all reviews.

        Returns:
            list: A list of all reviews with HTTP 200 status.
        """
        # Récupère les reviews dans le _storage
        reviews = facade.get_all_reviews()
        reviews_list = []                  # Crée une liste vide
        for review in reviews:             # Boucle dans le storage
            reviews_list.append({          # Ajoute chaque review dans la liste
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            })

        return reviews_list, 200           # Return la liste


# ----------------------- Route GET, PUT & DELETE : /api/v1/reviews/<review_id>
@api.route('/<review_id>')             # Création d'une route
class ReviewResource(Resource):        # Récupération des méthodes par Resource
    """Resource for retrieving, updating, and deleting a review by its ID."""
    @api.response(200, 'Review details retrieved successfully')     # OK
    @api.response(400, 'Invalid input data')                        # NOK
    @api.response(404, 'Review not found')                          # NOK
# -------------------------------- Fonction pour récupérer un review par son id
    def get(self, review_id):
        """
        Get review details by ID.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            dict: Review details with HTTP 200 on success,
                  or error message with HTTP 404 or 400 on failure.
        """
        try:
            # Récupère l'id par la façade
            review = facade.get_review(review_id)
            if not review:                      # Si la review n'est pas trouvé
                return {'error': 'Review not found'}, 404           # Erreur
            return {                            # Sinon retourne le review
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            }, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

# ----------------------- Route GET, PUT & DELETE : /api/v1/reviews/<review_id>
    # Vérifie avec review_update_model
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')       # OK
    @api.response(404, 'Review not found')                  # NOK
    @api.response(400, 'Invalid input data')                # NOK
# --------------------------------- Fonction pour modifier un review par son id
    def put(self, review_id):
        """
        Update a review's information.

        Args:
            review_id (str): The ID of the review to update.

        Expects JSON payload matching review_update_model.

        Returns:
            dict: Updated review data with HTTP 200 on success,
                  or error message with HTTP 400 or 404 on failure.
        """

        update_data = api.payload                  # Récupère nouvelles données
        try:
            # Vérifie les nouvelles données et si OK modifie le review
            updated_review = facade.update_review(review_id, update_data)
            if not updated_review:                      # Si review pas trouvé
                return {'error': 'Review not found'}, 404   # Erreur
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating
            }, 200                                          # Modification OK
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

# ----------------------- Route GET, PUT & DELETE : /api/v1/reviews/<review_id>
    @api.response(204, 'Review deleted successfully')           # OK
    @api.response(404, 'Review not found')                      # NOK
# -------------------------------- Fonction pour supprimer un review par son id
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Args:
            review_id (str): The unique identifier of the review to delete.

        Returns:
            dict: Success or error message with appropriate HTTP status code.
        """
        # Vérifie si le review existe et si OK supprime le review
        success = facade.delete_review(review_id)
        if not success:                            # Si échec return une erreur
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 204


# ------------------------------- Route GET : /api/v1/places/<place_id>/reviews
@api.route('/places/<place_id>/reviews')                # Création d'une route
class ReviewsByPlace(Resource):        # Récupération des méthodes par Resource
    """Resource to retrieve all reviews for a specific place."""
    @api.response(200, 'List of reviews for the specified place')   # OK
    @api.response(404, 'Place not found')                           # NOK
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        Args:
            place_id (str): The ID of the place.

        Returns:
            list: List of reviews for the place with HTTP 200,
                  or error message with HTTP 404 if place not found.
        """
        place = facade.get_place(place_id)      # Récupère la place par son id
        if not place:                  # Si la place n'est pas trouvée = Erreur
            return {'error': 'Place not found'}, 400
        # Récupère les reviews via l'id de la place
        reviews = facade.get_reviews_by_place(place_id)
        reviews_place_list = []
        for review in reviews:
            reviews_place_list.append({
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            })
        return reviews_place_list, 200          # Return la liste
