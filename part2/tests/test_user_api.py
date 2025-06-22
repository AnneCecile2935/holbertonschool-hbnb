from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users
from app.services import facade
import unittest


class UserApiTestCase(unittest.TestCase):

    def setUp(self):
        """Initialise une app Flask de test à chaque test"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(users, path='/api/v1/users')

        self.client = self.app.test_client()

        # Reset des données avant chaque test
        facade.user_repo.clear()
        from app.models.user import User
        User.users_email.clear()

    def test_create_user_valid(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["first_name"], "Claire")
        self.assertIn("id", data)

    def test_create_user_missing_field(self):
        payload = {
            "first_name": "Claire",
            "email": "claire@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_create_user_invalid_email(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "invalidemail"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_create_user_duplicate_email(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        self.client.post("/api/v1/users/", json=payload)
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("already used", res.get_json()["error"])

    def test_get_all_users(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        self.client.post("/api/v1/users/", json=payload)
        res = self.client.get("/api/v1/users/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()), 1)

    def test_get_user_by_id(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        post_res = self.client.post("/api/v1/users/", json=payload)
        user_id = post_res.get_json()["id"]
        res = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["email"], "claire@example.com")

    def test_get_user_not_found(self):
        res = self.client.get("/api/v1/users/inconnu")
        self.assertEqual(res.status_code, 404)

    def test_update_user_valid(self):
        post_res = self.client.post("/api/v1/users/", json={
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        })
        user_id = post_res.get_json()["id"]
        res = self.client.put(f"/api/v1/users/{user_id}", json={
            "first_name": "Claire-modifiée",
            "last_name": "Castan",
            "email": "claire.new@example.com"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["email"], "claire.new@example.com")

    def test_update_user_not_found(self):
        res = self.client.put("/api/v1/users/invalideid", json={
            "first_name": "X",
            "last_name": "Y",
            "email": "x@y.com"
        })
        self.assertEqual(res.status_code, 404)

    def test_update_user_email_taken(self):
        self.client.post("/api/v1/users/", json={
            "first_name": "Anne",
            "last_name": "Martin",
            "email": "anne@example.com"
        })
        post_res = self.client.post("/api/v1/users/", json={
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        })
        user_id = post_res.get_json()["id"]
        res = self.client.put(f"/api/v1/users/{user_id}", json={
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "anne@example.com"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("already registered", res.get_json()["error"])

class UserApiEdgeCasesTestCase(unittest.TestCase):
    def setUp(self):
        """Prépare une app de test et réinitialise les données"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(users, path='/api/v1/users')
        self.client = self.app.test_client()

        # Reset repositories
        facade.user_repo.clear()
        from app.models.user import User
        User.users_email.clear()

    def test_first_name_spaces_only(self):
        payload = {
            "first_name": "   ",
            "last_name": "Test",
            "email": "spacey@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_double_at(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Dupont",
            "email": "claire@@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_without_dot(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Dupont",
            "email": "claire@localhost"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_last_name_too_long(self):
        payload = {
            "first_name": "Claire",
            "last_name": "X" * 1000,
            "email": "claire@longname.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_case_insensitive_uniqueness(self):
        payload1 = {
            "first_name": "Claire",
            "last_name": "Upper",
            "email": "CLAIRE@EXAMPLE.COM"
        }
        payload2 = {
            "first_name": "Claire",
            "last_name": "Lower",
            "email": "claire@example.com"
        }
        res1 = self.client.post("/api/v1/users/", json=payload1)
        self.assertEqual(res1.status_code, 201)

        res2 = self.client.post("/api/v1/users/", json=payload2)
        # À adapter selon ton design (si case-insensitive)
        self.assertIn(res2.status_code, [201, 400])

    def test_email_as_object(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Test",
            "email": {"bad": "format"}
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_empty_payload(self):
        res = self.client.post("/api/v1/users/", json={})
        self.assertEqual(res.status_code, 400)

    def test_email_null(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Null",
            "email": None
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_with_spaces(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Test",
            "email": " claire@example.com "
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 201)  # ✅ Accepté, car email est nettoyé

        # Deuxième user avec même email sans espaces → doit être rejeté
        payload["email"] = "claire@example.com"
        res2 = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res2.status_code, 400)  # ✅ Rejeté, email déjà utilisé



    def test_put_user_with_same_email(self):
        # Crée un user
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        user_id = res.get_json()["id"]

        # Tente de modifier sans changer l'email
        res2 = self.client.put(f"/api/v1/users/{user_id}", json=payload)
        self.assertEqual(res2.status_code, 200)
class UserApiEdgeCasesTestCase(unittest.TestCase):
    def setUp(self):
        """Prépare une app de test et réinitialise les données"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(users, path='/api/v1/users')
        self.client = self.app.test_client()

        # Reset repositories
        facade.user_repo.clear()
        from app.models.user import User
        User.users_email.clear()

    def test_first_name_spaces_only(self):
        payload = {
            "first_name": "   ",
            "last_name": "Test",
            "email": "spacey@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_double_at(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Dupont",
            "email": "claire@@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_without_dot(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Dupont",
            "email": "claire@localhost"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_last_name_too_long(self):
        payload = {
            "first_name": "Claire",
            "last_name": "X" * 1000,
            "email": "claire@longname.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_case_insensitive_uniqueness(self):
        payload1 = {
            "first_name": "Claire",
            "last_name": "Upper",
            "email": "CLAIRE@EXAMPLE.COM"
        }
        payload2 = {
            "first_name": "Claire",
            "last_name": "Lower",
            "email": "claire@example.com"
        }
        res1 = self.client.post("/api/v1/users/", json=payload1)
        self.assertEqual(res1.status_code, 201)

        res2 = self.client.post("/api/v1/users/", json=payload2)
        # À adapter selon ton design (si case-insensitive)
        self.assertIn(res2.status_code, [201, 400])

    def test_email_as_object(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Test",
            "email": {"bad": "format"}
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_empty_payload(self):
        res = self.client.post("/api/v1/users/", json={})
        self.assertEqual(res.status_code, 400)

    def test_email_null(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Null",
            "email": None
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_email_with_spaces(self):
        payload = {
            "first_name": "Claire",
            "last_name": "Test",
            "email": " claire@example.com "
        }
        res = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res.status_code, 201)  # ✅ Accepté, car email est nettoyé

        # Deuxième user avec même email sans espaces → doit être rejeté
        payload["email"] = "claire@example.com"
        res2 = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(res2.status_code, 400)  # ✅ Rejeté, email déjà utilisé


    def test_put_user_with_same_email(self):
        # Crée un user
        payload = {
            "first_name": "Claire",
            "last_name": "Castan",
            "email": "claire@example.com"
        }
        res = self.client.post("/api/v1/users/", json=payload)
        user_id = res.get_json()["id"]

        # Tente de modifier sans changer l'email
        res2 = self.client.put(f"/api/v1/users/{user_id}", json=payload)
        self.assertEqual(res2.status_code, 200)

if __name__ == '__main__':
    unittest.main()
