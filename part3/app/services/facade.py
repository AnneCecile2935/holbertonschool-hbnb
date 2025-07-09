from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repositories.user_repository import UserRepository
from werkzeug.exceptions import BadRequest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        # Les methodes génériques sont importées
        # par héritage aux methodes spécifiques
        self.user_repository = UserRepository()
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

# -------------------------------------------------------- methodes facade user

    def create_user(self, user_data):
        # Passe les données dans les méthodes de classe
        try:
            user = User(**user_data)                     # Appel la classe User
        except (ValueError, TypeError) as e:             # Si NOK
            raise ValueError(f"Invalid user data: {str(e)}")  # Return erreur

        self.user_repository.add(user)         # Si OK ajout du user à la table
        return user                            # Return user

    def get_user_by_email(self, email):        # Récupère un user par son email
        return self.user_repository.get_user_by_email(email)

    def get_all_users(self):              # Récupère et retourne tout les users
        return self.user_repository.get_all()

    def get_user(self, user_id):          # Récupère et retourne l'user id
        return self.user_repository.get(user_id)

    def update_user(self, user_id, update_data):     # Modifie un user
        user = self.get_user(user_id)                # Récupère le user_id
        if not user:                                 # Vérifie si il existe
            raise ValueError("User not found")       # Si NOK return erreur
        if 'email' in update_data:           # Vérifie si il y un champ 'email'
            email = update_data['email']             # Récupère le new email
            existing_user = self.get_user_by_email(email)       # Vérifie email
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Email '{email}' is already registered.")

        # Boucle pour vérifier les Key et modifier les attributs dynamiquement
        allowed_fields = {"first_name", "last_name", "email"}
        for key in update_data:
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")

        self.user_repository.update(user_id, update_data)
        return user
# ----------------------------------------------------- methodes facade amenity

    def create_amenity(self, amenity_data):
        try:                    # Passe les données dans les méthodes de classe
            amenity = Amenity(**amenity_data)
        except (ValueError, TypeError) as e:                        # Si erreur
            raise ValueError(f"Invalid amenity data: {str(e)}")

        self.amenity_repository.add(amenity)             # Si OK ont ajoute l'amenity
        return amenity                             # Return user

    def get_amenity_by_name(self, name):
        # Récupère et return l'amenity par sont name
        return self.amenity_repository.get_by_attribute('name', name)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()   # Récup et return tout les amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)  # Récup et return amenity id

    def update_amenity(self, amenity_id, update_data):
        # Récupère l'obj amenity par son id
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:                    # Si l'amenity n'existe pas = Erreur
            raise ValueError("Amenity not found")
        try:
            # Mise à jour de l'amenity dans le repo
            self.amenity_repository.update(amenity_id, update_data)
        except (ValueError, TypeError) as e:
            raise BadRequest(str(e))

        return amenity

    def get_amenities_by_place(self, place_id):
        # Exemple où chaque amenity a une liste des place_ids associées
        amenities_list = []
        for amenity in self.amenity_repository.get_all():
            # Supposons que amenity a un attribut place_ids qui est une liste d'IDs
            if place_id in amenity.get('place_ids', []):
                amenities_list.append({
                    'id': amenity['id'],
                    'name': amenity['name']
                })
        return amenities_list

# ------------------------------------------------------- methodes facade place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_reviews_by_place(self, place_id):
        all_reviews = self.review_repository.get_all()  # Récupère toutes les reviews
        filtered_reviews = []                     # Liste vide

        for review in all_reviews:                # Boucle sur les reviews
            if review.place_id == place_id:       # Si place_id OK
                filtered_reviews.append(review)   # Ajoute la review à la liste

        return filtered_reviews                   # Return la liste

    def create_place(self, place_data):
        # Si le champ owner est vide ou si la place_data n'a pas de value
        # = Erreur
        if 'owner' not in place_data or not place_data["owner"]:
            raise ValueError("The place data must include an 'owner'.")

        owner_id = place_data['owner']    # Récupération de l'owner id
        owner = self.get_user(owner_id)   # Récupération de l'user id
        if not owner:                     # Si il n'y a pas de match = Erreur
            raise ValueError(f"Owner user with id {owner_id} does not exist.")

        place_data.pop('owner', None)     # Supprime l'entrée si elle existe
        try:
            # Passe les données dans les méthodes de classe
            place = Place(**place_data, owner=owner)
            self.place_repository.add(place)    # Ajout de la place dans le storage
            return place                  # Return l'objet
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid place data: {str(e)}")

    def get_all_places(self):
        return self.place_repository.get_all()  # Récup et return tout les places

    def update_place(self, place_id, place_data):
        # Récupère l'obj place par son id
        place = self.place_repository.get(place_id)
        if not place:                       # Si la place n'existe pas = Erreur
            raise ValueError("Place not found")

        # Boucle pour vérifier les Keys
        allowed_fields = {'title', 'description', 'price'}
        for key in place_data:
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")
        # Si ok modifie la BDD
        self.place_repository.update(place_id, place_data)
        return place
# ------------------------------------------------------ methodes facade review

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews linked to a specific place.

        Parameters:
            place_id: The unique ID of the place.

        Returns:
            list[Review]: List of reviews for the place.
        """
        return [
            review for review in self.review_repository.get_all()
            if review.place_id == place_id
        ]

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
        place = self.place_repository.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        user = self.user_repository.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        try:
            review = Review(
                review_data.get('text'),
                review_data.get('rating'),
                place,
                user
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid review: {str(e)}")
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.

        Parameters:
            review_id: The unique ID of the review.

        Returns:
            Review or None: The review instance if found, else None.
        """

        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            list[Review]: List of all reviews.
        """
        return self.review_repository.get_all()

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
            review.user = user

        if 'place_id' in update_data:
            place = self.get_place(update_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review.place = place

        # Boucle pour vérifier les Key et modifier les attributs dynamiquement
        allowed_fields = {'text', 'rating'}
        for key in update_data:
            if key not in allowed_fields:
                raise ValueError(f"Unexpected field: {key}")

        self.review_repository.update(review_id, update_data)
        return review

    def delete_review(self, review_id):
        """
        Delete a review from the repository by its ID.

        Parameters:
            review_id (str): The unique identifier of the review to delete.

        Returns:
            bool: True if the review was found and deleted, False otherwise.
        """
        review = self.review_repository.get(review_id)
        if not review:
            return False
        self.review_repository.delete(review_id)
        return True

    def get_review_by_id(self, review_id):
        return self.review_repository.get(review_id)

