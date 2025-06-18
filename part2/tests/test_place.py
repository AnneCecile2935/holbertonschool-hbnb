import unittest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

class TestPlaceModel(unittest.TestCase):
    def test_place_creation(self):
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )

        # Ajout d’un avis
        review = Review(text="Great stay!", rating=5, place=place, user=owner)
        place.add_review(review)

        # Assertions
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100)
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")

if __name__ == '__main__':
    unittest.main()
