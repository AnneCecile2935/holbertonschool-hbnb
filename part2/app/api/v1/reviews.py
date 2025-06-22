from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.api.v1 import users, amenities
from flask import request

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model(
    'Review',
    {
        'place_id': fields.String(
            required=True,
            description='ID of the place the review is about'
        ),
        'user_id': fields.String(
            required=True,
            description='ID of the user who made the review'
        ),
        'text': fields.String(
            required=True,
            description='The content of the review'
        ),
        'rating': fields.Integer(
            required=True,
            description='Rating between 1 and 5'
        )
    }
)
review_update_model = api.model(
    'ReviewUpdate',
    {
        'text': fields.String(
            required=True,
            description='The content of the review'
        ),
        'rating': fields.Integer(
            required=True,
            description='Rating between 1 and 5'
        )
    }
)
place_model = api.model(
    'Place',
    {
        'title': fields.String(
            required=True,
            description='Title of the place'
        ),
        'description': fields.String(
            description='Description of the place'
        ),
        'price': fields.Float(
            required=True,
            description='Price per night'
        ),
        'latitude': fields.Float(
            required=True,
            description='Latitude of the place'
        ),
        'longitude': fields.Float(
            required=True,
            description='Longitude of the place'
        ),
        'owner_id': fields.String(
            required=True,
            description='ID of the owner'
        ),
        'owner': fields.Nested(
            users,
            description='Owner of the place'
        ),
        'amenities': fields.List(
            fields.Nested(amenities),
            description='List of amenities'
        ),
        'reviews': fields.List(
            fields.Nested(review_model),
            description='List of reviews'
        )
    }
)


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id,
                'text': new_review.text,
                'rating': new_review.rating
            }, 201

        except (ValueError, TypeError) as e:
    # Check if the error message is about a missing place or user
            error_msg = str(e).lower()
            if "place not found" in error_msg or "user not found" in error_msg:
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            })

        return reviews_list, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return {
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            }, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""

        update_data = api.payload
        try:
            updated_review = facade.update_review(review_id, update_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Parameters:
            review_id (str): The unique identifier of the review to delete.

        Returns:
            tuple: A JSON message indicating success or failure and
            the corresponding HTTP status code.

        Responses:
            200: Review deleted successfully.
            404: Review not found.
        """
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class ReviewsByPlace(Resource):
    @api.response(200, 'List of reviews for the specified place')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ], 200
