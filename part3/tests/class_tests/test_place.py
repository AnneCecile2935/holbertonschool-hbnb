import unittest
import uuid
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class TestPlaceModel(unittest.TestCase):
    def setUp(self):
        """Configure test app and create a clean in-memory database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.owner = User(
            first_name="Alice",
            last_name="Smith",
            email=f"john_{uuid.uuid4()}@example.com",
            password="securepass"
        )
        db.session.add(self.owner)
        db.session.commit()

    def tearDown(self):
        """Remove session and drop all tables after test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

# ------------------------------------------------------------ Tests de base 🧪
    def test_place_creation_minimal(self):
        place = Place(
            title="Cozy Studio",
            price=50,
            latitude=48.85,
            longitude=2.35,
            owner=self.owner
        )
        db.session.add(place)
        db.session.commit()

        self.assertEqual(place.title, "Cozy Studio")
        self.assertEqual(place.owner_id, self.owner.id)
        self.assertIsNone(place.description)

    def test_place_with_review(self):
        place = Place(
            title="Flat with view",
            price=75,
            latitude=40.7,
            longitude=-74.0,
            owner=self.owner
        )
        review = Review(
            text="Awesome place!",
            rating=5,
            user=self.owner,
            place=place
        )
        db.session.add_all([place, review])
        db.session.commit()

        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Awesome place!")

    def test_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            _ = Place(
                title="Cheap Room",
                price=-10,  # 👈 déclenche l'erreur dans le setter Python
                latitude=20,
                longitude=30,
                owner=self.owner
            )

    def test_invalid_latitude_type(self):
        with self.assertRaises(TypeError):
            _ = Place(
                title="Odd Place",
                price=80,
                latitude="forty eight",
                longitude=2,
                owner=self.owner
            )

# ----------------------------------------------------------- Tests sournois 😈
    def test_empty_title_raises_error(self):
        with self.assertRaises(TypeError):
            _ = Place(
                title="   ",
                price=10,
                latitude=10,
                longitude=10,
                owner=self.owner
            )

    def test_long_title_raises_error(self):
        with self.assertRaises(ValueError):
            _ = Place(
                title="A" * 101,
                price=10,
                latitude=10,
                longitude=10,
                owner=self.owner
            )

    def test_description_none_is_allowed(self):
        place = Place(
            title="Simple",
            price=100,
            latitude=50,
            longitude=8,
            owner=self.owner,
            description=None
        )
        db.session.add(place)
        db.session.commit()
        self.assertIsNone(place.description)


if __name__ == "__main__":
    unittest.main()
