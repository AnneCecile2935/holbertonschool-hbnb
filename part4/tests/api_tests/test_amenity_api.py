
import unittest
from app import create_app

app = create_app()

class AmenityApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.base_url = "/api/v1/amenities/"

    def test_create_amenity_valid(self):
        data = {"name": "Wi-Fi"}
        response = self.client.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_amenity_missing_name(self):
        response = self.client.post(self.base_url, json={})
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        self.client.post(self.base_url, json={"name": "Pool"})
        self.client.post(self.base_url, json={"name": "Parking"})
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_amenity_by_id(self):
        post = self.client.post(self.base_url, json={"name": "AC"})
        amenity_id = post.get_json()["id"]
        response = self.client.get(f"{self.base_url}{amenity_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "AC")

    def test_get_amenity_not_found(self):
        response = self.client.get(f"{self.base_url}invalid-id")
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_valid(self):
        post = self.client.post(self.base_url, json={"name": "TV"})
        amenity_id = post.get_json()["id"]
        update = self.client.put(f"{self.base_url}{amenity_id}", json={"name": "Smart TV"})
        self.assertEqual(update.status_code, 200)
        self.assertEqual(update.get_json()["name"], "Smart TV")

    def test_update_amenity_invalid_data(self):
        post = self.client.post(self.base_url, json={"name": "Radio"})
        amenity_id = post.get_json()["id"]
        response = self.client.put(f"{self.base_url}{amenity_id}", json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_with_empty_name(self):
        """Should fail to create amenity with empty name"""
        response = self.client.post('/api/v1/amenities/', json={'name': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_create_amenity_with_missing_name(self):
        """Should fail to create amenity with no name field"""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.get_json())  # Correction ici
        self.assertIn('name', response.get_json()['errors'])  # Optionnel mais plus précis

    def test_update_amenity_with_empty_name(self):
        # Créer un amenity valide
        post = self.client.post('/api/v1/amenities/', json={'name': 'WiFi'})
        self.assertEqual(post.status_code, 201)
        amenity_id = post.get_json()['id']

        # Tenter une mise à jour avec un nom vide
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={'name': ''})
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_invalid_id(self):
        """Should return 404 when amenity ID does not exist"""
        response = self.client.get('/api/v1/amenities/invalid-id-123')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

if __name__ == "__main__":
    unittest.main()
