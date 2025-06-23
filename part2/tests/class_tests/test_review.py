import unittest
from unittest.mock import Mock
from app.models.review import Review  

class TestReview(unittest.TestCase):

    def setUp(self):
        # Création de faux objets place et user avec un attribut 'id'
        self.mock_place = Mock()
        self.mock_place.id = "place123"
        self.mock_place.add_review = Mock()

        self.mock_user = Mock()
        self.mock_user.id = "user123"

    def test_valid_initialization(self):
        review = Review("Great place!", 5, self.mock_place, self.mock_user)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, "place123")
        self.assertEqual(review.user, "user123")
        self.mock_place.add_review.assert_called_once_with(review)

    def test_invalid_text_type(self):
        with self.assertRaises(TypeError):
            Review(123, 4, self.mock_place, self.mock_user)

    def test_empty_text(self):
        with self.assertRaises(TypeError):
            Review("   ", 4, self.mock_place, self.mock_user)

    def test_invalid_rating_type(self):
        with self.assertRaises(TypeError):
            Review("Nice", "five", self.mock_place, self.mock_user)

    def test_invalid_rating_value(self):
        with self.assertRaises(ValueError):
            Review("Nice", 6, self.mock_place, self.mock_user)

    def test_place_missing_id(self):
        invalid_place = Mock()
        del invalid_place.id  # Supprimer l'attribut id
        with self.assertRaises(TypeError):
            Review("Nice", 4, invalid_place, self.mock_user)

    def test_user_missing_id(self):
        invalid_user = Mock()
        del invalid_user.id  # Supprimer l'attribut id
        with self.assertRaises(TypeError):
            Review("Nice", 4, self.mock_place, invalid_user)

    def test_text_setter_validation(self):
        review = Review("Nice", 4, self.mock_place, self.mock_user)
        with self.assertRaises(TypeError):
            review.text = 123
        with self.assertRaises(TypeError):
            review.text = "   "

    def test_rating_setter_validation(self):
        review = Review("Nice", 4, self.mock_place, self.mock_user)
        with self.assertRaises(TypeError):
            review.rating = "bad"
        with self.assertRaises(ValueError):
            review.rating = 10

if __name__ == '__main__':
    unittest.main()
