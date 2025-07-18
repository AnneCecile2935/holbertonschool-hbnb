import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models.base_model import BaseModel

class DummyModel(BaseModel):
    __tablename__ = "dummy_model"
    some_attr = db.Column(db.String(128), default="")

class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialise une app Flask + BDD en mémoire pour les tests."""
        cls.app = create_app()
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Active le contexte d'application (Flask)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Crée toutes les tables définies par les modèles
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.obj = DummyModel()
        self.obj.some_attr = "initial"
        db.session.add(self.obj)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

# ------------------------------------------------------------ Tests de base 🧪

    def test_id_is_string(self):
        self.assertIsInstance(self.obj.id, str)

    def test_created_and_updated_are_datetime(self):
        self.assertIsInstance(self.obj.created_at, datetime)
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_update_modifies_field_and_updates_timestamp(self):
        old = self.obj.updated_at
        time.sleep(0.01)
        self.obj.update({"some_attr": "updated"})
        self.assertEqual(self.obj.some_attr, "updated")
        self.assertGreater(self.obj.updated_at, old)

    def test_update_invalid_field_raises(self):
        with self.assertRaises(AttributeError):
            self.obj.update({"nonexistent_field": "value"})

# ----------------------------------------------------------- Tests sournois 😈

    def test_update_with_none_value(self):
        self.obj.update({"some_attr": None})
        self.assertIsNone(self.obj.some_attr)

    def test_update_with_empty_string(self):
        self.obj.update({"some_attr": ""})
        self.assertEqual(self.obj.some_attr, "")

    def test_update_with_unicode_characters(self):
        special = "🌟💡©️"
        self.obj.update({"some_attr": special})
        self.assertEqual(self.obj.some_attr, special)

    def test_update_updated_at_always_increasing(self):
        previous = self.obj.updated_at
        for value in ["a", "b", "c"]:
            time.sleep(0.01)
            self.obj.update({"some_attr": value})
            self.assertGreater(self.obj.updated_at, previous)
            previous = self.obj.updated_at

if __name__ == "__main__":
    unittest.main()
