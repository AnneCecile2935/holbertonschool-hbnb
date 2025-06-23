import unittest
from app import create_app
import uuid

class PlaceApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        self.user_data = {
            "first_name": "Test",
            "last_name": "Owner",
            "email": unique_email
        }
        user_resp = self.app.post("/api/v1/users/", json=self.user_data)
        print("User creation failed:", user_resp.status_code, user_resp.get_json())
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json()["id"]

    def test_create_place_valid(self):
        place_data = {
            "title": "Nice house",
            "description": "A beautiful house by the beach",
            "price": 100.5,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner": self.user_id
        }
        resp = self.app.post("/api/v1/places/", json=place_data)
        self.assertEqual(resp.status_code, 201)
        json_data = resp.get_json()
        self.assertEqual(json_data["title"], "Nice house")

    def test_create_place_missing_owner(self):
        place_data = {
            "title": "Orphan house",
            "description": "No owner",
            "price": 80.0,
            "latitude": 50.0,
            "longitude": 3.0
        }
        resp = self.app.post("/api/v1/places/", json=place_data)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_blank_title(self):
        place_data = {
            "title": "",
            "description": "Blank title",
            "price": 90.0,
            "latitude": 45.0,
            "longitude": 3.0,
            "owner": self.user_id
        }
        resp = self.app.post("/api/v1/places/", json=place_data)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_invalid_latitude(self):
        place_data = {
            "title": "Wrong latitude",
            "description": "Test",
            "price": 100.0,
            "latitude": "not a float",
            "longitude": 2.3,
            "owner": self.user_id
        }
        resp = self.app.post("/api/v1/places/", json=place_data)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_string_price(self):
        place_data = {
            "title": "Invalid price",
            "description": "Test",
            "price": "cheap",
            "latitude": 40.0,
            "longitude": 2.3,
            "owner": self.user_id
        }
        resp = self.app.post("/api/v1/places/", json=place_data)
        self.assertEqual(resp.status_code, 400)

    def test_get_all_places(self):
        resp = self.app.get("/api/v1/places/")
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.get_json(), list)

    def test_get_place_by_id(self):
        place_data = {
            "title": "Fetch house",
            "description": "Fetch it",
            "price": 60.0,
            "latitude": 50.0,
            "longitude": 1.0,
            "owner": self.user_id
        }
        post = self.app.post("/api/v1/places/", json=place_data)
        place_id = post.get_json()["id"]

        resp = self.app.get(f"/api/v1/places/{place_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["title"], "Fetch house")

    def test_get_place_not_found(self):
        resp = self.app.get("/api/v1/places/unknown_id")
        self.assertEqual(resp.status_code, 404)

    def test_update_place_valid(self):
        place_data = {
            "title": "Old title",
            "description": "Desc",
            "price": 120.0,
            "latitude": 45.0,
            "longitude": 5.0,
            "owner": self.user_id
        }
        post = self.app.post("/api/v1/places/", json=place_data)
        place_id = post.get_json()["id"]

        update = {"title": "New title"}
        resp = self.app.put(f"/api/v1/places/{place_id}", json=update)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["title"], "New title")

    def test_update_place_invalid_field(self):
        place_data = {
            "title": "Will break",
            "description": "Test",
            "price": 70.0,
            "latitude": 45.0,
            "longitude": 5.0,
            "owner": self.user_id
        }
        post = self.app.post("/api/v1/places/", json=place_data)
        place_id = post.get_json()["id"]

        update = {"latitude": "not a float"}
        resp = self.app.put(f"/api/v1/places/{place_id}", json=update)
        self.assertEqual(resp.status_code, 400)

    def test_update_place_with_invalid_price(self):
        place_data = {
            "title": "Price error",
            "description": "Bad price",
            "price": 150.0,
            "latitude": 42.0,
            "longitude": 3.0,
            "owner": self.user_id
        }
        post = self.app.post("/api/v1/places/", json=place_data)
        place_id = post.get_json()["id"]

        update = {"price": "free"}
        resp = self.app.put(f"/api/v1/places/{place_id}", json=update)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_missing_title(self):
        payload = {
            'description': 'No title',
            'price': 90,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner': self.user_id
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_title_as_number(self):
        payload = {
            'title': 12345,
            'description': 'Bad title type',
            'price': 90,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner': self.user_id
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_negative_price(self):
        payload = {
            'title': 'Cheap place',
            'description': 'Too cheap to be real',
            'price': -20,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner': self.user_id
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_invalid_owner(self):
        payload = {
            'title': 'Nice spot',
            'description': 'But ghost owner',
            'price': 100,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner': 'ghost-user-id'
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_extra_fields(self):
        payload = {
            'title': 'With extra',
            'description': 'Should fail or ignore',
            'price': 110,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner': self.user_id,
            'surprise': '🎁'
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertIn(resp.status_code, (200, 400))

    def test_update_place_with_invalid_latitude(self):
        post = self.app.post('/api/v1/places/', json={
            'title': 'Test lat',
            'description': 'Valid first',
            'price': 100,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner': self.user_id
        })
        place_id = post.get_json()['id']
        resp = self.app.put(f'/api/v1/places/{place_id}', json={'latitude': 'north'})
        self.assertEqual(resp.status_code, 400)

    def test_update_place_with_owner_field(self):
        post = self.app.post('/api/v1/places/', json={
            'title': 'My Place',
            'description': 'Nice one',
            'price': 100,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner': self.user_id
        })
        place_id = post.get_json()['id']
        resp = self.app.put(f'/api/v1/places/{place_id}', json={'owner': 'new-owner-id'})
        self.assertEqual(resp.status_code, 400)

    def test_create_place_with_empty_fields(self):
        payload = {
            'title': '',
            'description': '',
            'price': 100,
            'latitude': 48.85,
            'longitude': 2.35,
            'owner': self.user_id
        }
        resp = self.app.post('/api/v1/places/', json=payload)
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()
