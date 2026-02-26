import unittest
import json
from app import create_app


class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def test_01_create_user_success(self):
        data = {"first_name": "Alice", "last_name": "Dupont", "email": "alice@test.com"}
        res = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 201)
        body = res.get_json()
        self.assertIn("id", body)
        self.assertNotIn("password", body)

    def test_02_create_user_duplicate_email(self):
        data = {"first_name": "Alice", "last_name": "Dupont", "email": "alice2@test.com"}
        self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        res = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_03_create_user_invalid_email(self):
        data = {"first_name": "Bob", "last_name": "Martin", "email": "not-an-email"}
        res = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_04_create_user_missing_field(self):
        data = {"first_name": "Bob"}
        res = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_05_get_all_users(self):
        res = self.client.get("/api/v1/users/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_06_get_user_by_id(self):
        data = {"first_name": "Carol", "last_name": "Smith", "email": "carol@test.com"}
        created = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        user_id = created.get_json()["id"]
        res = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(res.status_code, 200)

    def test_07_get_user_not_found(self):
        res = self.client.get("/api/v1/users/nonexistent-id")
        self.assertEqual(res.status_code, 404)

    def test_08_update_user(self):
        data = {"first_name": "Dave", "last_name": "Lee", "email": "dave@test.com"}
        created = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        user_id = created.get_json()["id"]
        update = {"first_name": "David", "last_name": "Lee", "email": "dave@test.com"}
        res = self.client.put(f"/api/v1/users/{user_id}", data=json.dumps(update), headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["first_name"], "David")

    def test_09_create_amenity_success(self):
        data = {"name": "WiFi"}
        res = self.client.post("/api/v1/amenities/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["name"], "WiFi")

    def test_10_create_amenity_missing_name(self):
        res = self.client.post("/api/v1/amenities/", data=json.dumps({}), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_11_get_all_amenities(self):
        res = self.client.get("/api/v1/amenities/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_12_get_amenity_not_found(self):
        res = self.client.get("/api/v1/amenities/nonexistent-id")
        self.assertEqual(res.status_code, 404)

    def test_13_update_amenity(self):
        data = {"name": "Pool"}
        created = self.client.post("/api/v1/amenities/", data=json.dumps(data), headers=self.headers)
        amenity_id = created.get_json()["id"]
        res = self.client.put(f"/api/v1/amenities/{amenity_id}", data=json.dumps({"name": "Swimming Pool"}), headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["name"], "Swimming Pool")

    def _create_user(self, email="owner@test.com"):
        data = {"first_name": "Owner", "last_name": "Test", "email": email}
        res = self.client.post("/api/v1/users/", data=json.dumps(data), headers=self.headers)
        return res.get_json()["id"]

    def test_14_create_place_success(self):
        owner_id = self._create_user("owner1@test.com")
        data = {"title": "Nice flat", "price": 80.0, "latitude": 48.85, "longitude": 2.35, "owner_id": owner_id}
        res = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_15_create_place_invalid_owner(self):
        data = {"title": "Nice flat", "price": 80.0, "latitude": 48.85, "longitude": 2.35, "owner_id": "fake-id"}
        res = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_16_create_place_invalid_price(self):
        owner_id = self._create_user("owner2@test.com")
        data = {"title": "Bad place", "price": -10, "latitude": 48.85, "longitude": 2.35, "owner_id": owner_id}
        res = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_17_create_place_invalid_latitude(self):
        owner_id = self._create_user("owner3@test.com")
        data = {"title": "Bad place", "price": 50, "latitude": 999, "longitude": 2.35, "owner_id": owner_id}
        res = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_18_get_place_with_details(self):
        owner_id = self._create_user("owner4@test.com")
        data = {"title": "Cozy studio", "price": 60.0, "latitude": 48.85, "longitude": 2.35, "owner_id": owner_id}
        created = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        place_id = created.get_json()["id"]
        res = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(res.status_code, 200)
        body = res.get_json()
        self.assertIn("owner", body)
        self.assertIn("amenities", body)

    def test_19_get_place_not_found(self):
        res = self.client.get("/api/v1/places/nonexistent-id")
        self.assertEqual(res.status_code, 404)

    def _create_place(self, email="rev_owner@test.com"):
        owner_id = self._create_user(email)
        data = {"title": "Test place", "price": 50.0, "latitude": 48.85, "longitude": 2.35, "owner_id": owner_id}
        res = self.client.post("/api/v1/places/", data=json.dumps(data), headers=self.headers)
        return res.get_json()["id"], owner_id

    def test_20_create_review_success(self):
        place_id, user_id = self._create_place("rev1@test.com")
        data = {"text": "Great place!", "rating": 5, "place_id": place_id, "user_id": user_id}
        res = self.client.post("/api/v1/reviews/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_21_create_review_invalid_rating(self):
        place_id, user_id = self._create_place("rev2@test.com")
        data = {"text": "Bad rating", "rating": 10, "place_id": place_id, "user_id": user_id}
        res = self.client.post("/api/v1/reviews/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_22_create_review_invalid_place(self):
        owner_id = self._create_user("rev3@test.com")
        data = {"text": "No place", "rating": 3, "place_id": "fake-id", "user_id": owner_id}
        res = self.client.post("/api/v1/reviews/", data=json.dumps(data), headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_23_get_reviews_by_place(self):
        place_id, user_id = self._create_place("rev4@test.com")
        data = {"text": "Loved it!", "rating": 4, "place_id": place_id, "user_id": user_id}
        self.client.post("/api/v1/reviews/", data=json.dumps(data), headers=self.headers)
        res = self.client.get(f"/api/v1/reviews/places/{place_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_24_delete_review(self):
        place_id, user_id = self._create_place("rev5@test.com")
        data = {"text": "To delete", "rating": 2, "place_id": place_id, "user_id": user_id}
        created = self.client.post("/api/v1/reviews/", data=json.dumps(data), headers=self.headers)
        review_id = created.get_json()["id"]
        res = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(res.status_code, 200)
        res2 = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(res2.status_code, 404)

    def test_25_delete_review_not_found(self):
        res = self.client.delete("/api/v1/reviews/nonexistent-id")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
