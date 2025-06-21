"""
Module defining the HBnB facade for centralized access to data repositories.

This module introduces the `HBnBFacade` class, which groups together
the various repository interfaces:
    - users
    - places
    - reviews
    - amenities
and serves as a single entry point for the application's
business logic operations.

This structure helps encapsulate business logic and simplifies
interactions between the API layer and the persistence layer.
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    """
    Facade centralizing access to the HBnB application's repositories.

    Attributes:
    - user_repo: In-memory repository for users.
    - place_repo: In-memory repository for places.
    - review_repo: In-memory repository for reviews.
    - amenity_repo: In-memory repository for amenities.

    This class will contain the core business methods
    to interact with these repositories (create, retrieve, update, etc.).
    """
    def __init__(self):
        """
        Initializes the facade with in-memory repositories for each entity.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Creates a new user from the provided data.

        Parameter:
        - user_data: Dictionary containing the user's information.

        Note:
        - The implementation logic will be added in a future task.
        """
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required to create a user")
        existing_user = self.get_user_by_email(email)
        if existing_user is not None:
            raise ValueError(f"Email '{email}' is already registered.")
        try:
            user = User(**user_data)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid user data: {str(e)}")

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by their unique ID.

        Parameters:
            user_id: The unique identifier of the user.

        Returns:
            User or None: The user instance if found, else None.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.

        Parameters:
            email (str): The user's email.

        Returns:
            User or None: The user instance if found, else None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieve all users.

        Returns:
            list[User]: List of all user instances.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """
        Update an existing user's data.

        Parameters:
            user_id: The ID of the user to update.
            update_data (dict): Dictionary with fields to update.

        Returns:
            User: The updated user instance.

        Raises:
            ValueError: If user not found or email already registered
            by another user.
        """
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if 'email' in update_data:
            email = update_data['email']
            existing_user = self.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Email '{email}' is already registered.")

        for field in ['first_name', 'last_name', 'email']:
            if field in update_data:
                setattr(user, field, update_data[field])
        return user

    def get_place(self, place_id):
        """
        Retrieves a place by its unique identifier.

        Parameter:
        - place_id: The unique ID of the place.

        Returns:
        - The corresponding place object, or None if not found
          (logic to be implemented).
        """

        return self.place_repo.get(place_id)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews linked to a specific place.

        Parameters:
            place_id: The unique ID of the place.

        Returns:
            list[Review]: List of reviews for the place.
        """
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def create_place(self, place_data):
        """
        Create a new place with the given data.

        Parameters:
            place_data (dict): Data for the new place, must include 'owner' key with user ID.

        Returns:
            Place: The created Place instance.

        Raises:
            ValueError: If 'owner' is missing or owner user does not exist.
        """

        if 'owner' not in place_data:
            raise ValueError("The place data must include an 'owner'.")

        owner_id = place_data['owner']
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"Owner user with id {owner_id} does not exist.")

        place_data = place_data.copy()
        place_data.pop('owner')

        place = Place(**place_data, owner=owner)
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        """
        Retrieve all places.

        Returns:
            list[Place]: List of all place instances.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update an existing place's data.

        Parameters:
            place_id: The ID of the place to update.
            place_data (dict): Data fields to update.

        Returns:
            Place: The updated place instance.

        Raises:
            ValueError: If place not found.
        """

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        for field in ['title', 'description', 'price', 'latitude', 'longitude' ]:
            if field in place_data:
                setattr(place, field, place_data[field])
        return place

    def create_amenity(self, amenity_data, update_data):
        """
        Create a new amenity.

        Parameters:
            amenity_data (dict): Must contain 'name'.

        Returns:
            Amenity: The created Amenity instance.

        Raises:
            ValueError: If name is invalid or already registered.
        """
        name = amenity_data.get('name')
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # On ne fait plus de strip ici, c'est géré dans Amenity.name setter

        if self.get_amenity_by_name(name):
            raise ValueError(f"Name '{name}' is already registered.")

        try:
            amenity = Amenity(name=name)  # La validation et strip sont dans Amenity
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid amenity data: {str(e)}")

        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Parameters:
            amenity_id: The unique ID of the amenity.

        Returns:
            Amenity or None: The amenity instance if found, else None.
        """

        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by name.

        Parameters:
            name (str): Name of the amenity.

        Returns:
            Amenity or None: The amenity instance if found, else None.
        """
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        """
        Retrieve all amenities.

        Returns:
            list[Amenity]: List of all amenities.
        """

        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity's data.

        Parameters:
            amenity_id: The ID of the amenity to update.
            amenity_data (dict): Data fields to update.

        Returns:
            Amenity: The updated amenity instance.

        Raises:
            ValueError: If amenity not found, or name invalid or duplicated.
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            name = amenity_data['name']
            if not name or not isinstance(name, str):
                raise ValueError("Name must be a non-empty string")

            existing = self.get_amenity_by_name(name)
            if existing and existing.id != amenity_id:
                raise ValueError(f"Name '{name}' is already used.")

            amenity.name = name  # Le strip et validation sont dans le setter

        self.amenity_repo.update(amenity)
        return amenity

    def create_review(self, review_data):
        """
        Create a new review.

        Parameters:
            review_data (dict): Data for the new review, must include
            'place_id' and 'user_id'.

        Returns:
            Review: The created Review instance.

        Raises:
            ValueError: If place or user not found.
        """
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        review = Review(
            review_data.get('text'),
            review_data.get('rating'),
            place,
            user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.

        Parameters:
            review_id: The unique ID of the review.

        Returns:
            Review or None: The review instance if found, else None.
        """

        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            list[Review]: List of all reviews.
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, update_data):
        """
        Update an existing review.

        Parameters:
            review_id: The ID of the review to update.
            update_data (dict): Data fields to update.

        Returns:
            Review or None: The updated review instance, or None if not found.

        Raises:
            ValueError: If referenced user or place not found.
        """
        review = self.get_review(review_id)
        if not review:
            return None

        if 'user_id' in update_data:
            user = self.get_user(update_data['user_id'])
            if not user:
                raise ValueError("User not found")
            review.user_id = update_data['user_id']

        if 'place_id' in update_data:
            place = self.get_place(update_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review.place_id = update_data['place_id']

        for field in ['text', 'rating']:
            if field in update_data:
                setattr(review, field, update_data[field])
        return review
