🧾 Amenity API Test Log Documentation
This document provides a detailed log of tests conducted on the /api/v1/amenities/ endpoint. Each entry includes the tested endpoint, input data, expected and actual results, and any issues encountered.

## ✅ Summary Table

| #  | Test Description                             | Endpoint Tested                         | Input Data                             | Expected Result                      | Actual Result     | Issues Found |
|----|-----------------------------------------------|------------------------------------------|----------------------------------------|--------------------------------------|-------------------|--------------|
| 1  | Create amenity with valid name                | POST /api/v1/amenities/                  | { "name": "Wi-Fi" }                    | 201 Created with amenity ID          | ✅ As expected     | ❌           |
| 2  | Create amenity without a name                 | POST /api/v1/amenities/                  | {}                                     | 400 Bad Request                       | ✅ As expected     | ❌           |
| 3  | Get all amenities                             | GET /api/v1/amenities/                   | None                                   | 200 OK, list of amenities            | ✅ As expected     | ❌           |
| 4  | Get amenity by valid ID                       | GET /api/v1/amenities/{id}               | ID from valid creation                 | 200 OK, returns amenity with name    | ✅ As expected     | ❌           |
| 5  | Get amenity by invalid ID                     | GET /api/v1/amenities/invalid-id         | Invalid ID                             | 404 Not Found                         | ✅ As expected     | ❌           |
| 6  | Update amenity with valid name                | PUT /api/v1/amenities/{id}               | { "name": "Smart TV" }                 | 200 OK, name updated                  | ✅ As expected     | ❌           |
| 7  | Update amenity with empty name                | PUT /api/v1/amenities/{id}               | { "name": "" }                         | 400 Bad Request                       | ✅ As expected     | ❌           |
| 8  | Create amenity with empty name                | POST /api/v1/amenities/                  | { "name": "" }                         | 400 Bad Request                       | ✅ As expected     | ❌           |
| 9  | Create amenity with missing name field        | POST /api/v1/amenities/                  | {}                                     | 400 Bad Request with name error       | ✅ As expected     | ❌           |
| 10 | Update amenity with empty name after creation | PUT /api/v1/amenities/{id}               | { "name": "" }                         | 400 Bad Request                       | ✅ As expected     | ❌           |
| 11 | Get amenity with clearly invalid ID format    | GET /api/v1/amenities/invalid-id-123     | None                                   | 404 Not Found                         | ✅ As expected     | ❌           |

📌 Notes
All test cases returned the expected status codes and behavior.

The validation for empty or missing name fields is working correctly both on creation and update.

No bugs, regressions, or unhandled edge cases were encountered during this test cycle.

🧪 Recommendation
The Amenity API meets all tested functional and validation requirements. It handles both happy paths and error conditions appropriately. This implementation is considered stable for production assuming all dependent services behave as expected.
