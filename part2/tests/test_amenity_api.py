from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities
from app.models.amenity import Amenity
from app.services import facade
from app import create_app
import unittest

class AmenityApiTestCase(unittest.TestCase):
    def setUp(self):
        """Initialize Flask app and test client"""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        facade.amenity_repo.clear()
        Amenity.amenities_name.clear()

    def test_create_valid_amenity(self):
        """Test successful creation of an amenity"""
        response = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], 'Wi-Fi')

    def test_create_amenity_with_empty_name(self):
        """Test creation fails with empty name"""
        response = self.client.post('/api/v1/amenities/', json={'name': '   '})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_create_amenity_with_duplicate_name(self):
        """Test creation fails with duplicate name"""
        self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        response = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('already registered', response.json['error'])

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        self.client.post('/api/v1/amenities/', json={'name': 'Parking'})
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_amenity_by_id(self):
        """Test retrieving one amenity by ID"""
        post = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        amenity_id = post.json['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Wi-Fi')

    def test_get_amenity_not_found(self):
        """Test error when amenity ID does not exist"""
        response = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.json['error'].lower())

    def test_update_amenity_valid(self):
        """Test updating an amenity with valid data"""
        post = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        amenity_id = post.json['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={'name': 'Fibre'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Fibre')

    def test_update_amenity_duplicate_name(self):
        """Test update fails with duplicate name"""
        self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        post2 = self.client.post('/api/v1/amenities/', json={'name': 'TV'})
        amenity_id = post2.json['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={'name': 'Wi-Fi'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('already registered', response.json['error'])

    def test_update_amenity_not_found(self):
        """Test update fails for unknown amenity"""
        response = self.client.put('/api/v1/amenities/unknown-id', json={'name': 'TV'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.json['error'].lower())

    def test_create_amenity_name_too_long(self):
        """Test error when amenity name exceeds 50 characters"""
        long_name = 'x' * 51
        response = self.client.post('/api/v1/amenities/', json={'name': long_name})
        self.assertEqual(response.status_code, 400)
        self.assertIn('too long', response.json['error'].lower())

    def test_create_amenity_name_as_object(self):
        """Test error when amenity name is not a string"""
        response = self.client.post('/api/v1/amenities/', json={'name': {'text': 'Wi-Fi'}})
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json)
        self.assertIn('name', response.json['errors'])
        self.assertIn('not of type', response.json['errors']['name'].lower())


    def test_update_amenity_invalid_type(self):
        """Test update fails with non-string name"""
        post = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        amenity_id = post.json['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={'name': 123})
        self.assertEqual(response.status_code, 400)
        self.assertIn('must be a string', response.json['error'].lower())


if __name__ == '__main__':
    unittest.main()
