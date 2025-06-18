import unittest
from app.models.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        # On nettoie les emails enregistrés entre les tests
        User.users_email.clear()
        self.user = User("Alice", "Smith", "alice@example.com")

    def test_valid_user_creation(self):
        self.assertEqual(self.user.first_name, "Alice")
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(self.user.email, "alice@example.com")
        self.assertFalse(self.user.is_admin)

    def test_first_name_validation(self):
        with self.assertRaises(ValueError):
            self.user.first_name = ""
        with self.assertRaises(TypeError):
            self.user.first_name = 123
        with self.assertRaises(ValueError):
            self.user.first_name = "A" * 51

    def test_last_name_validation(self):
        with self.assertRaises(ValueError):
            self.user.last_name = ""
        with self.assertRaises(ValueError):
            self.user.last_name = " " * 10
        with self.assertRaises(ValueError):
            self.user.last_name = "B" * 51

    def test_email_validation(self):
        with self.assertRaises(ValueError):
            self.user.email = "invalidemail"
        with self.assertRaises(ValueError):
            self.user.email = "missing@dot"
        with self.assertRaises(ValueError):
            self.user.email = ""

    def test_is_admin_setter(self):
        self.user.is_admin = True
        self.assertTrue(self.user.is_admin)

        with self.assertRaises(ValueError):
            self.user.is_admin = "yes"

    def test_email_strip_on_set(self):
        user = User("Test", "User", "   test@domain.com  ")
        self.assertEqual(user.email, "test@domain.com")


if __name__ == "__main__":
    unittest.main()
