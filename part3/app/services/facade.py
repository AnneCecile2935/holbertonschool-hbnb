"""
HBnBFacade module.

This module defines the HBnBFacade class, which acts as an interface between
the application logic and the database layer. It centralizes operations for
users, places, amenities, and reviews, handling validation, relationships,
and business rules.
"""
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repositories.user_repository import UserRepository
from werkzeug.exceptions import BadRequest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        """Initialize repositories for users, places, amenities, and reviews"""
        self.user_repository = UserRepository()
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

# -------------------------------------------------------- methodes facade user
    def create_user(self, user_data):
        """Create a new user after validation."""
        try:
            # Passe les données dans les méthodes de classe
            user = User(**user_data)
            # Vérifie si l'email est déjà utilisé 
            if self.get_user_by_email(user_data['email']):
                raise ValueError("This email is already registered.")
        except (ValueError, TypeError) as e:
            # Renvoie le bon message selon l'erreur
            raise ValueError(f"Invalid user data: {str(e)}")
        # Si OK ajout du user à la table
        self.user_repository.add(user)
        return user

    def get_user_by_email(self, email):
        """Get a user by their email."""
        return self.user_repository.get_user_by_email(email)

    def get_all_users(self):
        """Return a list of all users."""
        return self.user_repository.get_all()

    def get_user(self, user_id):
        """Get a user by their ID."""
        return self.user_repository.get(user_id)

    def update_user(self, user_id, update_data):
        """Update user data after checking permissions and validation."""
        # Récupère le user_id
        user = self.get_user(user_id)

        # Vérifie que le user existe
        if not user:
            raise ValueError("User not found")

        # Vérifie si le champ 'email' à été modifié
        if 'email' in update_data:
            # Récupère l'email
            email = update_data['email']
            # Recherche le user par sont email
            existing_user = self.get_user_by_email(email)
            # Vérifie si l'email existe déjà
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Email '{email}' is already registered.")

        # Stock les attributs modifiables autorisés
        allowed_fields = {"first_name", "last_name", "email"}

        # Vérifie si le champ password est modifié
        if 'password' in update_data:
            # Si admin ajout de l'attribut password aux attributs autorisés
            allowed_fields.add('password')

        # Vérifie les clefs modifié qu'elles soient autorisés
        for key in update_data:
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")

        # Si tout est OK modification de la mémoire et de la BDD
        self.user_repository.update(user_id, update_data)
        return user

# ----------------------------------------------------- methodes facade amenity
    def create_amenity(self, amenity_data):
        """Create a new amenity with validation."""
        # Récupère le 'name' de l'amenity
        name = amenity_data.get("name")

        # Vérifie si il existe déjà dans la BDD
        if self.get_amenity_by_name(name):
            raise ValueError("This amenity is already registered.")

        try:
            # Passe les données dans les méthodes de classe
            amenity = Amenity(**amenity_data)
        except (ValueError, TypeError) as e:
            # Renvoie le bon message selon l'erreur
            raise ValueError(f"Invalid amenity data: {str(e)}")
        # Si OK ont ajoute l'amenity
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by its name."""
        return self.amenity_repository.get_by_attribute('name', name)

    def get_all_amenities(self):
        """Return a list of all amenities."""
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id):
        """Get an amenity by its ID."""
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id, update_data):
        """Update an existing amenity after validation."""
        # Récupère l'obj amenity par son id
        amenity = self.amenity_repository.get(amenity_id)

        # Vérifie si l'amenity existe
        if not amenity:
            raise ValueError("Amenity not found")

        try:
            # Mise à jour de l'amenity dans le repo
            self.amenity_repository.update(amenity_id, update_data)
        except (ValueError, TypeError) as e:
            # Renvoie le bon message selon l'erreur
            raise BadRequest(str(e))
        return amenity

    def get_amenities_by_place(self, place_id):
        """Get all amenities associated with a specific place."""
        # Création d'une liste vide
        amenities_list = []

        # Boucle pour parcourir toutes les amenities de la BDD
        for amenity in self.amenity_repository.get_all():
            # Vérifie si l'une des places liées a le bon id
            for place in amenity.places:
                # Vérifie si l'id de la place match avec celui qu'on cherche
                if place.id == place_id:
                    # Ajoute l'amenity à la liste
                    amenities_list.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
                    # Si match pas besoin de chercher plus
                    break
        return amenities_list

# ------------------------------------------------------- methodes facade place
    def get_place(self, place_id):
        """Get a place by its ID."""
        return self.place_repository.get(place_id)

    def create_place(self, place_data):
        """Create a new place linked to its owner after validation."""
        # Vérifie si le champ owner est rempli
        if 'owner' not in place_data or not place_data["owner"]:
            raise ValueError("The place data must include an 'owner'.")

        # Récupération de l'owner id
        owner_id = place_data['owner']
        # Récupération de l'user id
        owner = self.get_user(owner_id)

        # Vérifie si il y a un match entre le owner_id et le user_id
        if not owner:
            raise ValueError(f"Owner user with id {owner_id} does not exist.")

        # Supprime l'entrée si elle existe
        place_data.pop('owner', None)

        try:
            # Passe les données dans les méthodes de classe
            place = Place(**place_data, owner=owner)
            # Ajout de la place dans le storage
            self.place_repository.add(place)
            return place
        except (TypeError, ValueError) as e:
            # Renvoie le bon message selon l'erreur
            raise ValueError(f"Invalid place data: {str(e)}")

    def get_all_places(self):
        """Return a list of all places."""
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        """Update place data after validation."""
        # Récupère l'obj place par son id
        place = self.place_repository.get(place_id)

        # Vérifie si la place existe
        if not place:
            raise ValueError("Place not found")

        # Stock les attributs modifiables autorisés
        allowed_fields = {'title', 'description', 'price'}

        # Boucle pour parcourir les champs modifiés
        for key in place_data:
            # Vérifie si les champs sont autorisés
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")

        # Si tout est OK -> modifie la BDD
        self.place_repository.update(place_id, place_data)
        return place

# ------------------------------------------------------ methodes facade review
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        # Création d'une liste vide
        reviews_place = []
        # Récupération de tout les reviews
        all_reviews = self.review_repository.get_all()

        # Boucle sur toutes les reviews de la BDD
        for review in all_reviews:
            # Vérifie si il y a match
            if review.place_id == place_id:
                # Ajoute la review à la liste
                reviews_place.append(review)
        return reviews_place

    def create_review(self, review_data):
        """Create a new review with validation and relational linking."""
        # Récupère la place
        place = self.place_repository.get(review_data['place_id'])

        # Vérifie si elle existe
        if not place:
            raise ValueError("Place not found")

        # Récupère le user
        user = self.user_repository.get(review_data['user_id'])

        # Vérifie si le user existe
        if not user:
            raise ValueError("User not found")

        try:
            # Récupère les données
            review = Review(
                review_data.get('text'),
                review_data.get('rating'),
                place,
                user
            )
        except (TypeError, ValueError) as e:
            # Gestion des messages selon l'erreur
            raise ValueError(f"Invalid review: {str(e)}")

        # Ajout de la review à la BDD
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by its ID."""
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Return a list of all reviews."""
        return self.review_repository.get_all()

    def update_review(self, review_id, update_data):
        """Update review data and linked user/place if necessary."""
        # Récupère la review
        review = self.get_review(review_id)

        # Vérifie si elle existe
        if not review:
            return None

        # Vérifie si le user_id des nouvelles données
        if 'user_id' in update_data:
            # Récupère le user par son id
            user = self.get_user(update_data['user_id'])
            # Vérifie si il existe
            if not user:
                raise ValueError("User not found")
            # Si OK lie la review au user
            review.user_obj = user
        # Vérifie l'id de la place des nouvelles données
        if 'place_id' in update_data:
            # Récupère la place par sont id
            place = self.get_place(update_data['place_id'])
            # Vérifie si elle existe
            if not place:
                raise ValueError("Place not found")
            # Si OK lie la review à la place
            review.place_obj = place

        # Stock les Keys des attributs dont la modif est autorisés
        allowed_fields = {'text', 'rating'}

        # Boucle pour vérifier les Keys modifiées
        for key in update_data:
            # Vérifie si ce sont des keys autorisées
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")

        # Si tout est OK modifie la BDD
        self.review_repository.update(review_id, update_data)
        return review

    def delete_review(self, review_id):
        """Delete a review by its ID."""
        # Récupère la review par son id
        review = self.review_repository.get(review_id)

        # Vérifie qu'elle existe
        if not review:
            raise ValueError("Review not found")

        # Suprrime la review
        self.review_repository.delete(review_id)
        return True

    def get_review_by_id(self, review_id):
        """Alias for getting a review by ID (duplicate of get_review)."""
        return self.review_repository.get(review_id)
