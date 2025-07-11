import unittest
from app import create_app, db
from app.models.amenity import Amenity


class TestAmenityModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start Flask app context and create tables."""
        cls.app = create_app()  # adapte si tu n’as pas ce mode
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up Flask app context and drop tables."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Rollback session before each test."""
        db.session.rollback()

    def tearDown(self):
        """Rollback session after each test."""
        db.session.rollback()

# ------------------------------------------------------------ Tests de base 🧪

    def test_valid_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        db.session.add(amenity)
        db.session.commit()
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_name_trimmed(self):
        amenity = Amenity(name="  Parking  ")
        self.assertEqual(amenity.name, "Parking")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            Amenity(name=" ")

    def test_name_too_long_raises(self):
        long_name = "x" * 51
        with self.assertRaises(ValueError):
            Amenity(name=long_name)

    def test_name_must_be_string(self):
        with self.assertRaises(TypeError):
            Amenity(name=123)

    def test_duplicate_name_raises(self):
        amenity1 = Amenity(name="Pool")
        db.session.add(amenity1)
        db.session.commit()

        with self.assertRaises(ValueError):
            amenity2 = Amenity(name="Pool")
            db.session.add(amenity2)
            db.session.commit()

    def test_repr_output(self):
        amenity = Amenity(name="Garden")
        self.assertIn("Amenity", repr(amenity))
        self.assertIn("Garden", repr(amenity))

# ----------------------------------------------------------- Tests Sournois 😈

    def test_none_name_raises(self):
        with self.assertRaises(TypeError):
            Amenity(name=None)

    def test_boolean_name_raises(self):
        with self.assertRaises(TypeError):
            Amenity(name=True)

    def test_whitespace_only_name_raises(self):
        with self.assertRaises(ValueError):
            Amenity(name="\t\n  ")

    def test_duplicate_name_with_spaces_raises(self):
        db.session.add(Amenity(name="Sauna"))
        db.session.commit()
        with self.assertRaises(ValueError):
            db.session.add(Amenity(name="  Sauna  "))
            db.session.commit()

    def test_name_with_special_characters(self):
        name = "🌟 Jacuzzi™ – Deluxe"
        amenity = Amenity(name=name)
        db.session.add(amenity)
        db.session.commit()
        self.assertEqual(amenity.name, name.strip())

    def test_multiple_invalid_adds(self):
        db.session.add(Amenity(name="Barbecue"))
        db.session.commit()

        with self.assertRaises(ValueError):
            db.session.add(Amenity(name=""))  # vide

        with self.assertRaises(ValueError):
            db.session.add(Amenity(name="Barbecue"))  # duplicata


if __name__ == '__main__':
    unittest.main()
