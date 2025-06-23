🧪 User API Test Report
📋 Endpoints Tested
HTTP Method	Endpoint	Description
POST	/api/v1/users/	Create a new user
GET	/api/v1/users/	Retrieve all users
GET	/api/v1/users/<id>	Retrieve a user by ID
PUT	/api/v1/users/<id>	Update an existing user

### 🧾 Test Summary

| #  | Test Description                                | Input Data (Example)                           | Expected Outcome                     | Actual Outcome     | Issues Found |
|----|--------------------------------------------------|------------------------------------------------|--------------------------------------|--------------------|--------------|
| 1  | Create valid user                                | `{first_name: "Alice", ...}`                   | 201 Created, return ID               | ✅ As expected      | ❌            |
| 2  | Create user with duplicate email                 | Same email twice                               | 400 Error with message               | ✅ As expected      | ❌            |
| 3  | Get all users                                    | None                                           | 200 OK, list of users                | ✅ As expected      | ❌            |
| 4  | Get user by ID                                   | Valid ID returned after creation               | 200 OK, correct user data            | ✅ As expected      | ❌            |
| 5  | Update user with valid data                      | Valid update payload                           | 200 OK, updated fields               | ✅ As expected      | ❌            |
| 6  | Update non-existent user                         | `/users/unknown-id`                            | 404 Not Found                        | ✅ As expected      | ❌            |
| 7  | Get non-existent user                            | `/users/nonexistent-id`                        | 404 Not Found                        | ✅ As expected      | ❌            |
| 8  | Create user with blank first name                | `"first_name": "   "`                          | 400 Bad Request                      | ✅ As expected      | ❌            |
| 9  | Create user with missing required fields         | Missing `first_name` and `last_name`           | 400 Bad Request                      | ✅ As expected      | ❌            |
| 10 | Create user with invalid email formats           | `noatsign.com`, `user@nodot`, `user@@double.com` | 400 Bad Request                    | ✅ As expected      | ❌            |
| 11 | Create user with too long first name             | `"first_name": "A"*200`                        | 400 Bad Request                      | ✅ As expected      | ❌            |
| 12 | Create user with boolean as email                | `"email": true`                                | 400 Bad Request                      | ✅ As expected      | ❌            |
| 13 | Create user with number as last name             | `"last_name": 123`                             | 400 Bad Request                      | ✅ As expected      | ❌            |
| 14 | Update user with blank first name                | `"first_name": "   "`                          | 400 Bad Request                      | ✅ As expected      | ❌            |
| 15 | Update user with invalid email format            | `"email": "bad-email"`                         | 400 Bad Request                      | ✅ As expected      | ❌            |
| 16 | Update user with too long last name              | `"last_name": "B"*200`                         | 400 Bad Request                      | ✅ As expected      | ❌            |
| 17 | Update user email to an existing one             | User A email assigned to User B                | 400 Bad Request                      | ✅ As expected      | ❌            |

🚧 Observations
✅ All tests passed successfully.

❗ No unexpected behavior or bugs were encountered.

🧹 Validation appears robust, handling edge cases like malformed input, duplicates, and invalid formats.

📌 Recommendations
Consider including additional validations (e.g., domain name validation in emails, regex strengthening).

Add tests for:

Deletion of users (DELETE /api/v1/users/<id>)

Pagination or filtering if supported in GET /api/v1/users/

🗂️ Conclusion
This test suite confirms that the /api/v1/users/ endpoint meets expected functional requirements with proper input validation, duplicate detection, and resource handling. The implementation is solid and ready for integration testing.

Let me know if you want this exported as a Markdown/HTML/PDF report or extended to other test suites.
