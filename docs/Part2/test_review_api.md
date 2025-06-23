# 🧪 Test Documentation — Review API

## 📍 Introduction

This test suite verifies the core functionalities and edge cases of the Review
API in a Flask application. It ensures that review creation, retrieval,
updating, and deletion behave as expected under both normal and erroneous
conditions.

Each test uses a fresh setup with a dynamically generated user and place,
created via the facade service, to maintain isolation and consistency across
tests.

## ✅ Summary Table – Review API

| #  | Test Description                              | Endpoint Tested                          | Input Data                                                                 | Expected Result                              | Actual Result     | Issues Found |
|----|-----------------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------|----------------------------------------------|-------------------|--------------|
| 1  | Create review with valid input                | POST /api/v1/reviews/                     | `{ "place_id": valid, "user_id": valid, "text": "Nice place!", "rating": 5 }` | 201 Created with review ID                   | ✅ As expected     | ❌           |
| 2  | Create review with missing text               | POST /api/v1/reviews/                     | `{ "place_id": valid, "user_id": valid, "rating": 5 }`                       | 400 Bad Request                               | ✅ As expected     | ❌           |
| 3  | Create review with rating outside range       | POST /api/v1/reviews/                     | `{ "text": "Nice", "rating": 10, ... }`                                     | 400 Bad Request                               | ✅ As expected     | ❌           |
| 4  | Update review with valid data                 | PUT /api/v1/reviews/{id}                  | `{ "text": "Updated", "rating": 4, ... }`                                   | 200 OK with updated review                    | ✅ As expected     | ❌           |
| 5  | Get review by valid ID                        | GET /api/v1/reviews/{id}                  | Review ID from creation                                                     | 200 OK with correct review data               | ✅ As expected     | ❌           |
| 6  | Delete existing review                        | DELETE /api/v1/reviews/{id}               | Review ID from creation                                                     | 204 No Content                                | ✅ As expected     | ❌           |
| 7  | Create review with invalid user ID            | POST /api/v1/reviews/                     | `{ "user_id": invalid, ... }`                                               | 400 Bad Request                               | ✅ As expected     | ❌           |
| 8  | Create review with invalid place ID           | POST /api/v1/reviews/                     | `{ "place_id": invalid, ... }`                                              | 400 Bad Request                               | ✅ As expected     | ❌           |
| 9  | Create review with integer text               | POST /api/v1/reviews/                     | `{ "text": 1234, ... }`                                                     | 400 Bad Request                               | ✅ As expected     | ❌           |
| 10 | Create review with empty string text          | POST /api/v1/reviews/                     | `{ "text": "", ... }`                                                       | 400 Bad Request                               | ✅ As expected     | ❌           |
| 11 | Create review with string rating              | POST /api/v1/reviews/                     | `{ "rating": "five", ... }`                                                 | 400 Bad Request                               | ✅ As expected     | ❌           |
| 12 | Create review with float rating               | POST /api/v1/reviews/                     | `{ "rating": 3.5, ... }`                                                    | 400 Bad Request                               | ✅ As expected     | ❌           |
| 13 | Create review with rating out of bounds       | POST /api/v1/reviews/                     | `{ "rating": 0 or 6, ... }`                                                 | 400 Bad Request                               | ✅ As expected     | ❌           |
| 14 | Update review with non-integer rating         | PUT /api/v1/reviews/{id}                  | `{ "rating": "three" }`                                                     | 400 Bad Request                               | ✅ As expected     | ❌           |
| 15 | Update review with unknown field              | PUT /api/v1/reviews/{id}                  | `{ "unknown_field": "???" }`                                                | 200 OK or 400 Bad Request (depends on logic)  | ✅ As expected     | ❌           |
| 16 | Create review with all null fields            | POST /api/v1/reviews/                     | `{ "text": null, "rating": null, ... }`                                     | 400 Bad Request                               | ✅ As expected     | ❌           |

## 📌 Conclusion

This test suite ensures the Review API:

Enforces validation on required fields and value ranges.

Properly handles incorrect or malformed requests.

Executes core CRUD operations reliably.
