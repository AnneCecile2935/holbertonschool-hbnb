import unittest
from datetime import datetime, timedelta
import time

from app.models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.obj = BaseModel()

    def test_id_is_string(self):
        self.assertIsInstance(self.obj.id, str)

    def test_created_and_update_at_are_datetime(self):
        self.assertIsInstance(self.obj.created_at, datetime)
        self.assertIsInstance(self.obj.update_at, datetime)

    def test_save_updates_update_at(self):
        old_update = self.obj.update_at
        time.sleep(0.001)
        self.obj.save()
        self.assertGreater(self.obj.update_at, old_update)

    def test_update_changes_attributes_and_calls_save(self):
        old_update = self.obj.update_at
        time.sleep(0.01)
        self.obj.some_attr = "old value"
        self.obj.update({"some_attr": "new value"})
        self.assertEqual(self.obj.some_attr, "new value")
        self.assertGreater(self.obj.update_at, old_update)

    def test_update_does_not_add_new_attributes(self):
        with self.assertRaises(AttributeError):
            self.obj.update({"new_attr": "value"})

if __name__ == '__main__':
    unittest.main()
