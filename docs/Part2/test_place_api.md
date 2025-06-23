# 🧪 Functional Test Report: Place API

## 📌 Introduction

This document provides a summary of functional tests executed against the Place
 API endpoints of the application. These tests were designed to validate both
valid and invalid use cases, covering common scenarios such as creation, retrieval,
and updating of place records. The purpose is to ensure the API behaves correctly
in handling various inputs, enforces data constraints, and maintains system integrity.

## ✅ Summary Table (Markdown)

| #  | Test Description                                | Endpoint Tested                      | Input Data (Example)                                                | Expected Result                           | Actual Result         | Issues Found |
|----|--------------------------------------------------|---------------------------------------|----------------------------------------------------------------------|--------------------------------------------|------------------------|--------------|
| 1  | Create valid place                              | POST `/api/v1/places/`                | title, description, price, lat/lon, valid owner ID                   | 201 Created, returns place ID              | ✅ As expected         | ❌           |
| 2  | Create place missing owner                      | POST `/api/v1/places/`                | Same as above, no `"owner"` key                                     | 400 Bad Request                            | ✅ As expected         | ❌           |
| 3  | Create place with blank title                   | POST `/api/v1/places/`                | title = `""`                                                         | 400 Bad Request                            | ✅ As expected         | ❌           |
| 4  | Create place with invalid latitude (string)     | POST `/api/v1/places/`                | latitude = `"not a float"`                                           | 400 Bad Request                            | ✅ As expected         | ❌           |
| 5  | Create place with price as string               | POST `/api/v1/places/`                | price = `"cheap"`                                                    | 400 Bad Request                            | ✅ As expected         | ❌           |
| 6  | Get all places                                  | GET `/api/v1/places/`                 | None                                                                 | 200 OK, returns list                       | ✅ As expected         | ❌           |
| 7  | Get place by valid ID                           | GET `/api/v1/places/{id}`            | ID of created place                                                  | 200 OK, returns matching place             | ✅ As expected         | ❌           |
| 8  | Get place by unknown ID                         | GET `/api/v1/places/unknown_id`       | invalid ID                                                           | 404 Not Found                              | ✅ As expected         | ❌           |
| 9  | Update place title                              | PUT `/api/v1/places/{id}`            | `{ "title": "New title" }`                                           | 200 OK, title updated                      | ✅ As expected         | ❌           |
| 10 | Update place with invalid field (latitude str)  | PUT `/api/v1/places/{id}`            | latitude = `"not a float"`                                           | 400 Bad Request                            | ✅ As expected         | ❌           |
| 11 | Update place with string price                  | PUT `/api/v1/places/{id}`            | price = `"free"`                                                     | 400 Bad Request                            | ✅ As expected         | ❌           |
| 12 | Create place with missing title                 | POST `/api/v1/places/`                | no `"title"` key                                                     | 400 Bad Request                            | ✅ As expected         | ❌           |
| 13 | Create place with numeric title                 | POST `/api/v1/places/`                | title = `12345`                                                      | 400 Bad Request                            | ✅ As expected         | ❌           |
| 14 | Create place with negative price                | POST `/api/v1/places/`                | price = `-20`                                                        | 400 Bad Request                            | ✅ As expected         | ❌           |
| 15 | Create place with invalid owner                 | POST `/api/v1/places/`                | owner = `"ghost-user-id"`                                            | 400 Bad Request                            | ✅ As expected         | ❌           |
| 16 | Create place with extra unexpected field        | POST `/api/v1/places/`                | includes `"surprise": "🎁"`                                          | 200 OK or 400 Bad Request (impl. specific) | ✅ As expected         | ❌           |
| 17 | Update place with invalid latitude              | PUT `/api/v1/places/{id}`            | latitude = `"north"`                                                 | 400 Bad Request                            | ✅ As expected         | ❌           |
| 18 | Update place trying to change owner             | PUT `/api/v1/places/{id}`            | owner = `"new-owner-id"`                                             | 400 Bad Request                            | ✅ As expected         | ❌           |
| 19 | Create place with all empty fields              | POST `/api/v1/places/`                | title = "", description = ""                                         | 400 Bad Request                            | ✅ As expected         | ❌           |

## 🧾 Conclusion

The test suite provides thorough validation of the Place API’s core functionalities.
 It verifies the handling of both standard and edge-case inputs.
 All tests produced expected results, and no functional defects were identified at this stage.
 The API demonstrates good resilience against malformed data and enforces business rules properly.
 This builds confidence in the reliability and integrity of the place creation and management features.

