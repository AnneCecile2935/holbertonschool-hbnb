import unittest
from app import create_app
import json

app = create_app()

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_user_valid(self):
        data = {
            "first_name": "Alice",
            "last_name": "Dupont",
            "email": "alice.dupont@example.com"
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_user_duplicate_email(self):
        data = {
            "first_name": "Bob",
            "last_name": "Martin",
            "email": "bob.martin@example.com"
        }
        self.client.post("/api/v1/users/", data=json.dumps(data),
                         content_type='application/json')
        # Reuse same email
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_all_users(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        data = {
            "first_name": "Charlie",
            "last_name": "Doe",
            "email": "charlie.doe@example.com"
        }
        post = self.client.post("/api/v1/users/", data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(post.status_code, 201)
        user_id = post.get_json()["id"]

        response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], user_id)

    def test_update_user_valid(self):
        data = {
            "first_name": "Diane",
            "last_name": "Lemoine",
            "email": "diane@example.com"
        }
        post = self.client.post("/api/v1/users/", data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(post.status_code, 201)
        user_id = post.get_json()["id"]

        update_data = {
            "first_name": "Diane",
            "last_name": "Durand",
            "email": "diane@example.com"
        }
        response = self.client.put(f"/api/v1/users/{user_id}", data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["last_name"], "Durand")

    def test_update_user_not_found(self):
        update_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@nowhere.com"
        }
        response = self.client.put("/api/v1/users/unknown-id", data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_user_not_found(self):
        response = self.client.get("/api/v1/users/nonexistent-id")
        self.assertEqual(response.status_code, 404)

    def test_create_user_with_blank_first_name(self):
        data = {
            "first_name": "   ",
            "last_name": "Dupont",
            "email": "blank@example.com"
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_missing_fields(self):
        data = {
            "email": "missing@example.com"
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_invalid_email_format(self):
        invalid_emails = [
            "noatsign.com",     # Pas de @
            "user@nodot",       # Pas de point
            "user@@double.com", # Double @
            # "@nouser.com",      # Manque nom
            # "user@.com"         # Domaine invalide
        ]
        for email in invalid_emails:
            data = {
                "first_name": "Test",
                "last_name": "Mail",
                "email": email
            }
            response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400, f"Failed for email: {email}")

    def test_create_user_with_very_long_first_name(self):
        data = {
            "first_name": "A" * 200,
            "last_name": "Durand",
            "email": "longname@example.com"
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_boolean_email(self):
        data = {
            "first_name": "Boolean",
            "last_name": "Test",
            "email": True
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_number_as_last_name(self):
        data = {
            "first_name": "Num",
            "last_name": 123,
            "email": "number@example.com"
        }
        response = self.client.post("/api/v1/users/", data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_user_blank_first_name(self):
        # Création d’un utilisateur valide
        data = {
            "first_name": "Marion",
            "last_name": "Claire",
            "email": "marion@example.com"
        }
        post = self.client.post("/api/v1/users/", data=json.dumps(data),
                                content_type='application/json')
        user_id = post.get_json()["id"]

        # Tentative de mise à jour avec un prénom vide
        update = {
            "first_name": "   ",
            "last_name": "Claire",
            "email": "marion@example.com"
        }
        resp = self.client.put(f"/api/v1/users/{user_id}", data=json.dumps(update),
                               content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_update_user_invalid_email_format(self):
        data = {
            "first_name": "Olivier",
            "last_name": "Test",
            "email": "olivier@example.com"
        }
        post = self.client.post("/api/v1/users/", data=json.dumps(data),
                                content_type='application/json')
        user_id = post.get_json()["id"]

        update = {
            "first_name": "Olivier",
            "last_name": "Test",
            "email": "bad-email"
        }
        resp = self.client.put(f"/api/v1/users/{user_id}", data=json.dumps(update),
                               content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_update_user_with_too_long_last_name(self):
        data = {
            "first_name": "Sarah",
            "last_name": "Normal",
            "email": "sarah@example.com"
        }
        post = self.client.post("/api/v1/users/", data=json.dumps(data),
                                content_type='application/json')
        user_id = post.get_json()["id"]

        update = {
            "last_name": "B" * 200,
            "email": "sarah@example.com"
        }
        resp = self.client.put(f"/api/v1/users/{user_id}", data=json.dumps(update),
                               content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_update_user_email_to_existing_email(self):
        # Création de 2 users
        data1 = {
            "first_name": "A",
            "last_name": "A",
            "email": "a@example.com"
        }
        data2 = {
            "first_name": "B",
            "last_name": "B",
            "email": "b@example.com"
        }
        post1 = self.client.post("/api/v1/users/", data=json.dumps(data1),
                                 content_type='application/json')
        post2 = self.client.post("/api/v1/users/", data=json.dumps(data2),
                                 content_type='application/json')
        id_1 = post1.get_json()["id"]
        id_2 = post2.get_json()["id"]

        # Tentative de modifier le 2e user avec l'email du 1er
        update = {
            "email": "a@example.com"
        }
        resp = self.client.put(f"/api/v1/users/{id_2}", data=json.dumps(update),
                               content_type="application/json")
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()
