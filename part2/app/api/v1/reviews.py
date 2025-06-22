"""
Reviews API module.

This module provides endpoints for managing reviews associated with places.
It supports creating, retrieving, updating, and deleting reviews,
as well as fetching all reviews for a specific place.

Endpoints:
- /api/v1/reviews/ [GET, POST]: List all reviews or create a new one.
- /api/v1/reviews/<review_id> [GET, PUT, DELETE]: Retrieve, update, or delete a specific review.
- /api/v1/reviews/places/<place_id>/reviews [GET]: Get all reviews for a given place.

Models:
- review_model: Schema for review creation and validation.
- review_update_model: Schema for review updates.
- place_model: Schema for places including nested owner, amenities, and reviews.
"""
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
    """Resource to create a new review and retrieve all reviews."""
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """
        Register a new review.

        Expects JSON payload matching review_model.
        Validates referenced place and user existence.

        Returns:
            dict: Created review data with HTTP 201 on success,
                  or error message with HTTP 400 or 404 on failure.
        """
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

            error_msg = str(e).lower()
            if "place not found" in error_msg or "user not found" in error_msg:
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        Returns:
            list: A list of all reviews with HTTP 200 status.
        """
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
    """Resource for retrieving, updating, and deleting a review by its ID."""
    @api.response(200, 'Review details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
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
        """
        Update a review's information.

        Args:
            review_id (str): The ID of the review to update.

        Expects JSON payload matching review_update_model.

        Returns:
            dict: Updated review data with HTTP 200 on success,
                  or error message with HTTP 400 or 404 on failure.
        """

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

        Args:
            review_id (str): The unique identifier of the review to delete.

        Returns:
            dict: Success or error message with appropriate HTTP status code.
        """
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class ReviewsByPlace(Resource):
    """Resource to retrieve all reviews for a specific place."""
    @api.response(200, 'List of reviews for the specified place')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        Args:
            place_id (str): The ID of the place.

        Returns:
            list: List of reviews for the place with HTTP 200,
                  or error message with HTTP 404 if place not found.
        """
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
