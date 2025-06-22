# 🧪 Test Process Documentation – Endpoints: User, Place, Review, Amenity

## 1. Objective

Verify the correct operation of the API endpoints related to the following entities:
- `User`: user management
- `Place`: place management
- `Review`: user reviews
- `Amenity`: features or amenities of a place

Each test covers:
- Standard use cases (CRUD)
- Edge / error cases
- Business rules (validation, data consistency)

---

## 2. Test Environment

| Element            | Tool / Version         |
|--------------------|------------------------|
| API Framework      | Flask + Flask-RESTx    |
| Testing Tools      | Swagger UI, Postman    |
| Database           | SQLite (local test)    |
| Test Method        | Manual / automated calls |
| Code Version       | Commit `v1.0` (branch `dev`) |

---

## 3. Test Cases by Entity

### 🧑‍💼 User

| ID   | Scenario                                | Input / Request                    | Expected Result               | Status |
|------|-----------------------------------------|------------------------------------|-------------------------------|--------|
| U01  | Valid user creation                     | `POST /users` + complete JSON      | 201 Created + user JSON       | ✅     |
| U02  | Creation with duplicate email           | Same email as an existing user     | 400 Bad Request               | ✅     |
| U03  | Retrieve existing user                  | `GET /users/<user_id>`             | 200 OK + user JSON            | ✅     |
| U04  | Retrieve non-existent user              | `GET /users/<fake_id>`             | 404 Not Found                 | ✅     |

---

### 🏠 Place

| ID   | Scenario                               | Request                            | Expected Result               | Status |
|------|----------------------------------------|------------------------------------|-------------------------------|--------|
| P01  | Create place with valid `owner`        | `POST /places` + JSON              | 201 Created + place JSON      | ✅     |
| P02  | Create place without `owner`           | JSON without `owner` field         | 400 Bad Request               | ✅     |
| P03  | Create place with invalid `owner` ID   | `owner = "invalid-id"`             | 404 Not Found                 | ✅     |
| P04  | Retrieve a place                       | `GET /places/<id>`                 | 200 OK                        | ✅     |
| P05  | Update a place (excluding owner)       | `PUT /places/<id>` + update JSON   | 200 OK                        | ✅     |
| P06  | Attempt to modify the `owner` field    | `PUT` request with `owner` field   | 400 Bad Request (rejected)    | ✅     |

---

### ✍️ Review

| ID   | Scenario                                  | Request                             | Expected Result              | Status |
|------|-------------------------------------------|-------------------------------------|------------------------------|--------|
| R01  | Valid review creation                     | `POST /reviews` + complete JSON     | 201 Created                  | ✅     |
| R02  | Creation with `rating` out of bounds      | `rating = 6`                        | 400 Bad Request              | ✅     |
| R03  | Creation with missing field               | JSON missing `text`                | 400 Bad Request              | ✅     |
| R04  | Retrieve existing review                  | `GET /reviews/<id>`                 | 200 OK                       | ✅     |
| R05  | Get all reviews for a place               | `GET /reviews/places/<place_id>`    | 200 OK + review list         | ✅     |
| R06  | Update review (rating & text)             | `PUT /reviews/<id>` + valid JSON    | 200 OK                       | ✅     |

---

### 🛠️ Amenity

| ID   | Scenario                                  | Request                             | Expected Result              | Status |
|------|-------------------------------------------|-------------------------------------|------------------------------|--------|
| A01  | Valid amenity creation                    | `POST /amenities` + JSON            | 201 Created                  | ✅     |
| A02  | Creation with missing `name` field        | JSON without `name`                 | 400 Bad Request              | ✅     |
| A03  | Retrieve an amenity                       | `GET /amenities/<id>`               | 200 OK                       | ✅     |
| A04  | List all amenities                        | `GET /amenities`                    | 200 OK + list                | ✅     |
| A05  | Delete an amenity                         | `DELETE /amenities/<id>`           | 204 No Content               | ✅     |
| A06  | Link between Amenity and Place (if any)   | `GET /places/<id>/amenities`        | 200 OK                       | ✅     |

---

## 4. Coverage Summary

| Entity   | Creation | Read (GET) | Update (PUT) | Delete (DELETE) | Business Validation     |
|----------|----------|------------|--------------|------------------|--------------------------|
| User     | ✅        | ✅          | –            | –                | ✅ (unique email)        |
| Place    | ✅        | ✅          | ✅           | –                | ✅ (`owner` required)    |
| Review   | ✅        | ✅          | ✅           | –                | ✅ (valid rating)        |
| Amenity  | ✅        | ✅          | –            | ✅               | ✅ (`name` required)     |

---

## 5. Suggested Future Improvements

- 🔐 Add authorization tests (e.g., only owners can update a place)
- ⚙️ Integrate into a full `pytest` suite
- 📊 Add performance testing for high-load scenarios
- 🧪 Use mocking for `facade` and `repository` layers to enable precise unit testing

---
