import unittest
from app import create_app
from app.services import facade
import uuid

class ReviewApiTestCase(unittest.TestCase):
    """Test case for the Review API endpoints"""

    def setUp(self):
        self.app = create_app().test_client()
        self.base_url = "/api/v1/reviews/"
        # Crée un user et un place de test
        self.user = facade.create_user({
            "first_name": "Bob",
            "last_name": "Morane",
            'email': f'{uuid.uuid4()}@example.com',
        })
        print("\n[DEBUG USER]", self.user)  # ✅ Affiche le user généré
        self.place = facade.create_place({
            'title': 'Test Place',
            'description': 'A test place',
            'price': 99.9,
            'latitude': 40.0,
            'longitude': 3.0,
            'owner': self.user.id
        })
        print("[DEBUG PLACE]", self.place)  # ✅ Affiche le place généré

    def test_create_review_valid(self):
        """Should create a valid review"""
        payload = {
            "place_id": self.place.id,
            "user_id": self.user.id,
            "text": "Nice place!",
            "rating": 5
        }
        resp = self.app.post(self.base_url, json=payload)
        print("[DEBUG REVIEW]", resp.status_code, resp.get_json())
        self.assertEqual(resp.status_code, 201)
        self.assertIn('id', resp.get_json())

    def test_create_review_missing_text(self):
        """Should fail if text is missing"""
        payload = {
            "place_id": self.place.id,
            "user_id": self.user.id,
            "rating": 5
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_invalid_rating(self):
        """Should fail if rating is not in [1,5]"""
        payload = {
            "place_id": self.place.id,
            "user_id": self.user.id,
            "text": "Nice place!",
            "rating": 10
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_update_review_valid(self):
        """Should update review properly"""
        post = self.app.post(self.base_url, json={
            "place_id": self.place.id,
            "user_id": self.user.id,
            "text": "Nice place!",
            "rating": 3
        })
        json_data = post.get_json()
        print("[DEBUG REVIEW]", post.status_code, json_data)

        if not json_data or 'id' not in json_data:
            self.fail("Review creation failed: missing 'id' in response")

        review_id = json_data['id']
        review_id = post.get_json()['id']
        resp = self.app.put(f'/api/v1/reviews/{review_id}', json={
            "place_id": self.place.id,
            "user_id": self.user.id,
            "text": "Updated",
            "rating": 4
        })
        print("[DEBUG POST REVIEW]", post.status_code, post.get_json())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['text'], 'Updated')
        self.assertEqual(resp.get_json()['rating'], 4)

    def test_get_review_by_id(self):
        """Should retrieve review by ID"""
        post = self.app.post(self.base_url, json={
            'text': 'Get me!',
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        json_data = post.get_json()
        print("[DEBUG REVIEW]", post.status_code, json_data)

        if not json_data or 'id' not in json_data:
            self.fail("Review creation failed: missing 'id' in response")

        review_id = json_data['id']
        #review_id = post.get_json()['id']
        get = self.app.get(f'/api/v1/reviews/{review_id}')
        print("[DEBUG POST REVIEW]", post.status_code, post.get_json())
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.get_json()['text'], 'Get me!')

    def test_delete_review_valid(self):
        """Should delete existing review"""
        post = self.app.post(self.base_url, json={
            'text': 'Delete me!',
            'rating': 2,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        json_data = post.get_json()
        print("[DEBUG REVIEW]", post.status_code, json_data)

        if not json_data or 'id' not in json_data:
            self.fail("Review creation failed: missing 'id' in response")

        review_id = json_data['id']
        #review_id = post.get_json()['id']
        delete = self.app.delete(f'/api/v1/reviews/{review_id}')
        print("[DEBUG POST REVIEW]", post.status_code, post.get_json())
        self.assertEqual(delete.status_code, 204)

    def test_create_review_invalid_user(self):
        """Should fail if user ID is unknown"""
        payload = {
            'text': 'Invalid user',
            'rating': 4,
            'user_id': str(uuid.uuid4()),
            'place_id': self.place.id
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_invalid_place(self):
        """Should fail if place ID is unknown"""
        payload = {
            'text': 'Invalid place',
            'rating': 4,
            'user_id': self.user.id,
            'place_id': str(uuid.uuid4())
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_with_text_as_int(self):
        """Should fail if text is an integer instead of a string"""
        payload = {
            'text': 1234,
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_with_empty_text(self):
        """Should fail if text is an empty string"""
        payload = {
            'text': '',
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_with_rating_as_string(self):
        """Should fail if rating is a string instead of int"""
        payload = {
            'text': 'Wrong rating type',
            'rating': 'five',
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_with_rating_as_float(self):
        """Should fail if rating is a float (even if in bounds)"""
        payload = {
            'text': 'Float rating',
            'rating': 3.5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_with_rating_out_of_bounds(self):
        """Should fail if rating is below 1 or above 5"""
        for bad_rating in [0, 6, -1, 999]:
            with self.subTest(rating=bad_rating):
                payload = {
                    'text': 'Bad rating',
                    'rating': bad_rating,
                    'user_id': self.user.id,
                    'place_id': self.place.id
                }
                resp = self.app.post(self.base_url, json=payload)
                self.assertEqual(resp.status_code, 400)

    def test_update_review_with_invalid_rating_type(self):
        """Should fail to update if rating is not an int"""
        post = self.app.post(self.base_url, json={
            'text': 'Initial',
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        json_data = post.get_json()
        print("[DEBUG REVIEW]", post.status_code, json_data)

        if not json_data or 'id' not in json_data:
            self.fail("Review creation failed: missing 'id' in response")

        review_id = json_data['id']
        review_id = post.get_json()['id']
        resp = self.app.put(f'/api/v1/reviews/{review_id}', json={
            'rating': 'three'
        })
        self.assertEqual(resp.status_code, 400)

    def test_update_review_with_unknown_field(self):
        """Should ignore or fail on unknown field"""
        post = self.app.post(self.base_url, json={
            'text': 'Initial',
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        json_data = post.get_json()
        print("[DEBUG REVIEW]", post.status_code, json_data)

        if not json_data or 'id' not in json_data:
            self.fail("Review creation failed: missing 'id' in response")

        review_id = json_data['id']
        review_id = post.get_json()['id']
        resp = self.app.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Still good',
            'unknown_field': '???'
        })
        # Tu peux décider ici si ton API doit échouer ou ignorer l'attribut inconnu
        self.assertIn(resp.status_code, (200, 400))

    def test_create_review_with_null_fields(self):
        """Should fail with None as value for required fields"""
        payload = {
            'text': None,
            'rating': None,
            'user_id': None,
            'place_id': None
        }
        resp = self.app.post(self.base_url, json=payload)
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()
