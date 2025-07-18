"""
Reviews API module.

This module provides endpoints for managing reviews associated with places.
It supports creating, retrieving, updating, and deleting reviews,
as well as fetching all reviews for a specific place.

Endpoints:
- /api/v1/reviews/ [GET, POST]: List all reviews or create a new one.
- /api/v1/reviews/<review_id> [GET, PUT, DELETE]: Retrieve, update, or delete
  a specific review.
- /api/v1/places/<place_id>/reviews [GET]: Get all reviews for a given place.

Models:
- review_model: Schema for review creation and validation.
- review_update_model: Schema for review updates.
- place_model: Schema for places including nested owner, amenities, and
  reviews.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.users import user_model
from app.api.v1.amenities import amenity_model
from app.utils.decorators import handle_errors

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
    """
    Resource to handle creation of new reviews and retrieval of all reviews.

    POST:
        Create a new review by an authenticated user.
        Validations:
            - The referenced place exists.
            - The user is not the owner of the place.
            - The user has not already reviewed this place.

    GET:
        Retrieve a list of all reviews.
    """
    @api.expect(review_model, validate=True)        # Vérifie avec review_model
    @api.response(201, 'Review successfully created')               # OK
    @api.response(400, 'Invalid input data')                        # NOK
    @api.response(400, 'User or Place not found')                   # NOK
    @handle_errors
    @jwt_required()
# ---------------------------------- Fonction pour enregister un nouveau review
    def post(self):
        """
        Create a new review.

        Requires JWT authentication. The user must not be the owner of the
        place, and must not have already reviewed the place.

        Request JSON payload:
            {
                "place_id": str,
                "user_id": str,
                "text": str,
                "rating": int (1-5)
            }

        Returns:
            201 with the created review data on success,
            400 if user is not allowed to review,
            404 if the place does not exist.
        """
        current_user = get_jwt_identity()
        # Récupère l'identité de l'utilisateur connecté via le token JWT
        user_id = current_user['id']
        review_data = api.payload      # Récup les datas envoyées par le client
        # Extrait l'ID du lieu depuis les données
        place_id = (
            review_data.get('place_id')
            if isinstance(review_data, dict)
            else review_data
        )
        # Vérifie si le lieu existe dans la base
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'place not found'}, 404
        # L'utilisateur ne peut pas commenter son propre lieu
        if place.owner == user_id:
            return {'error': 'You cannot review your own place'}, 400
        # Récupère les avis existants pour ce lieu
        existing_reviews = facade.get_reviews_by_place(place_id)
        # Vérifie si l'utilisateur a déjà laissé un avis pour ce lieu
        if any(review.user_id == user_id for review in existing_reviews):
            return {'error': 'You have already reviewed this place'}, 400
        # Si tout est valide, crée un nouvel avis avec les donnéesfournies
        new_review = facade.create_review(review_data)
        # Retourne les infos de l'avis créé sous forme de JSON
        return {
            'id': new_review.id,
            'place_id': new_review.place_id,
            'user_id': new_review.user_id,
            'text': new_review.text,
            'rating': new_review.rating
            }, 201                              # Création OK

# ----------------------------------------- Route POST & GET : /api/v1/reviews/
    @api.response(200, 'List of reviews retrieved successfully')
# -------------------------------- Fonction pour récupérer la liste des reviews
    def get(self):
        """
        Retrieve all reviews.

        Returns a list of all reviews with their details.

        Returns:
            200 with a list of reviews.
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
    """
    Resource for retrieving, updating, and deleting a review by its ID.

    GET:
        Retrieve review details by review ID.

    PUT:
        Update an existing review owned by the authenticated user.

    DELETE:
        Delete an existing review owned by the authenticated user.
    """
    @api.response(200, 'Review details retrieved successfully')     # OK
    @api.response(404, 'Review not found')                          # NOK
    @handle_errors
# -------------------------------- Fonction pour récupérer un review par son id
    def get(self, review_id):
        """
        Retrieve details of a specific review by ID.

        Args:
            review_id (str): Review ID to retrieve.

        Returns:
            200 with review data on success,
            404 if review not found.
        """
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

# ----------------------- Route GET, PUT & DELETE : /api/v1/reviews/<review_id>
    # Vérifie avec review_update_model
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')       # OK
    @api.response(404, 'Review not found')                  # NOK
    @handle_errors
    @jwt_required()
# --------------------------------- Fonction pour modifier un review par son id
    def put(self, review_id):
        """
        Update a review's content and rating.

        Requires JWT authentication. The user must own the review.

        Args:
            review_id (str): Review ID to update.

        Request JSON payload must match `review_update_model` schema:
            {
                "text": str,
                "rating": int (1-5)
            }

        Returns:
            200 with updated review data on success,
            403 if user does not own the review,
            404 if review not found,
            400 if payload invalid.
        """
        current_user = get_jwt_identity()
        user_id = current_user['id']
        # Try to find the review in the database
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': "Review not found"}, 404
        # Check if the current user is the owner of the review
        if str(review.user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403
        # Get the update data sent by the client

        updated_review = facade.update_review(review_id, api.payload)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating
        }, 200                                          # Modification OK

# ----------------------- Route GET, PUT & DELETE : /api/v1/reviews/<review_id>
    @api.response(200, 'Review deleted successfully')           # OK
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')                      # NOK
    @jwt_required()
# -------------------------------- Fonction pour supprimer un review par son id
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Requires JWT authentication. The user must own the review.

        Args:
            review_id (str): Review ID to delete.

        Returns:
            200 with success message on deletion,
            403 if user does not own the review,
            404 if review not found.
        """
        current_user = get_jwt_identity()
        user_id = current_user['id']
        review = facade.get_review_by_id(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        if review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        # Vérifie si le review existe et si OK supprime le review
        success = facade.delete_review(review_id)
        if not success:                            # Si échec return une erreur
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


# ------------------------------- Route GET : /api/v1/places/<place_id>/reviews
@api.route('/places/<place_id>/reviews')                # Création d'une route
class ReviewsByPlace(Resource):        # Récupération des méthodes par Resource
    """
    Resource to retrieve all reviews for a specific place.

    GET:
        Retrieve all reviews associated with the specified place ID.
    """
    @api.response(200, 'List of reviews for the specified place')   # OK
    @api.response(404, 'Place not found')                           # NOK
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        Args:
            place_id (str): ID of the place whose reviews are being requested.

        Returns:
            200: A list of reviews for the specified place.
            404: Error if the place is not found.
        """
        place = facade.get_place(place_id)      # Récupère la place par son id
        if not place:                  # Si la place n'est pas trouvée = Erreur
            return {'error': 'Place not found'}, 404
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
