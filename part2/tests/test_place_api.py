import unittest
from app import create_app
from app.services import facade
from app.models.user import User
import uuid

class PlaceApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        unique_email = f"{uuid.uuid4()}@example.com"
        self.user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.valid_place = {
            "title": "Cozy Cottage",
            "description": "A nice place in the woods",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 5.0,
            "owner": self.user.id
        }

    # ✅ TC1 : Créer un lieu valide
    def test_create_valid_place(self):
        response = self.app.post('/api/v1/places/', json=self.valid_place)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    # ✅ TC2 : Récupérer tous les lieux
    def test_get_all_places(self):
        self.app.post('/api/v1/places/', json=self.valid_place)
        response = self.app.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    # ✅ TC3 : Récupérer un lieu par ID
    def test_get_place_by_id(self):
        post = self.app.post('/api/v1/places/', json=self.valid_place)
        place_id = post.json['id']
        response = self.app.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], place_id)

    # ✅ TC4 : Modifier un lieu avec des données valides
    def test_update_place_valid(self):
        post = self.app.post('/api/v1/places/', json=self.valid_place)
        place_id = post.json['id']
        update = {"title": "Updated Cottage"}
        response = self.app.put(f'/api/v1/places/{place_id}', json=update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], "Updated Cottage")

    # 😈 TE1 : Créer un lieu sans owner
    def test_create_place_missing_owner(self):
        bad_data = self.valid_place.copy()
        del bad_data["owner"]
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("owner", response.json["error"].lower())

    # 😈 TE2 : Créer un lieu avec owner inexistant
    def test_create_place_invalid_owner(self):
        bad_data = self.valid_place.copy()
        bad_data["owner"] = "fake-id"
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json["error"].lower())

    # 😈 TE3 : Créer un lieu avec un titre vide
    def test_create_place_empty_title(self):
        bad_data = self.valid_place.copy()
        bad_data["title"] = ""
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)

    # 😈 TE4 : Créer un lieu avec prix négatif
    def test_create_place_negative_price(self):
        bad_data = self.valid_place.copy()
        bad_data["price"] = -10
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)

    # 😈 TE5 : Créer un lieu avec latitude hors plage
    def test_create_place_bad_latitude(self):
        bad_data = self.valid_place.copy()
        bad_data["latitude"] = 100.0
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)

    # 😈 TE6 : Créer un lieu avec longitude hors plage
    def test_create_place_bad_longitude(self):
        bad_data = self.valid_place.copy()
        bad_data["longitude"] = 200.0
        response = self.app.post('/api/v1/places/', json=bad_data)
        self.assertEqual(response.status_code, 400)

    # 😈 TE7 : Modifier un lieu inexistant
    def test_update_place_not_found(self):
        update = {"title": "Doesn't Matter"}
        response = self.app.put('/api/v1/places/unknown-id', json=update)
        self.assertEqual(response.status_code, 404)

    # 😈 TE8 : Modifier un champ owner
    def test_update_place_owner_forbidden(self):
        post = self.app.post('/api/v1/places/', json=self.valid_place)
        place_id = post.json['id']
        update = {"owner": "new-owner-id"}
        response = self.app.put(f'/api/v1/places/{place_id}', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not allowed", response.json["error"].lower())

if __name__ == '__main__':
    unittest.main()
