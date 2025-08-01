# HBnB - Part 4: Simple Web Client

This is Part 3 of the HBnB project, which introduces user authentication and database integration. It replaces in-memory storage with SQLAlchemy ORM using SQLite (for development) and MySQL (for production), and adds secure user login via JWT.

## 🎯 Objectives – Part 4

The main goals of Part 4 of the HBnB project are:

✅ Create an interactive front-end that matches provided design specifications.

✅ Connect the web client to the back-end API using Fetch and handle JSON responses.

✅ Implement login functionality with JWT token storage in browser cookies.

✅ Build dynamic pages: login, list of places, place detail, and review submission.

✅ Filter data client-side (e.g., by country) and conditionally display UI based on authentication.


## 📌 Features

- Responsive and modular front-end interface using HTML, CSS, and JS
- JWT-based login and session persistence via cookies
- Fetch integration to load and manipulate API data in real time
- Protected routes (e.g., add review requires login)
- Place filtering by country
- Display of all place reviews and review submission form
- Ability to update a place if the user is the owner

## 🗂️ Project Structure

```
<pre>

part4/
frontend/
├── index.html             # List of places (home page)
├── login.html             # Login form
├── place.html             # Place details and reviews
├── add_review.html        # Form to add a review
├── update_place.html      # Form to update a place
├── style.css              # App-wide styling
├── js/
│   ├── auth.js            # Authentication & token handling
│   ├── edit-place.js      # form to update a place
│   ├── index.js           # Home page logic (place listing)
│   ├── login.js           # Login logic
│   ├── main.js            # Principal script
│   ├── place.js           # Place detail and reviews logic
│   ├── review.js          # Submit a review for a place
│   └── utils.js           # Reusable helpers

</pre>
```

## 🖥️ Running the Full Application (Back-end + Front-end)

To run the complete HBnB application, you need to start both the back-end API server and the front-end static server.

🔙 Start the Back-end (Flask API)

```bash

### Activate virtual environment if needed

source venv/bin/activate
```

```bash
### Run the Flask back-end server

python3 run.py
```

By default, it runs at:

```arduino

http://localhost:5000/
```

🔜 Start the Front-end (Static Server)
You can use any static server (e.g., Python's http.server, Live Server, or serve via VSCode).

Example with Python:

```bash

cd front_end/
python3 -m http.server 5500
```

This will serve the HTML files at:

```arduino

http://localhost:5500/
```

Make sure your back-end is running at http://localhost:5000/ so the front-end can communicate properly with the API.

## ⚙️ Notes
CORS must be enabled on the Flask API to allow requests from the front-end.

The JWT token is stored as a cookie to persist the login session.

DOM updates are managed via vanilla JS (no front-end framework used).

Minimal external dependencies—pure HTML/CSS/JS.

---

## 🔐 Auth Flow

User logs in → token is stored in cookie.

All fetch calls include token in headers if user is authenticated.

User is redirected to login if token is missing or invalid.

Logout clears the cookie and redirects to login page.

## 🚧 Project Status

✅ Front-end pages implemented and styled
✅ JWT-based login integrated
✅ Place list and detail pages dynamically populated
✅ Review submission available to authenticated users
✅ Conditional rendering based on user session
✅ Edit Place feature for place owners
🕓 Responsive design improvements and animations pending

## 🧪 Technologies

- HTML5
- CSS3
- JavaScript (ES6)
- Fetch API
- JWT (stored in cookies)
- Flask (back-end) with CORS enabled

## 📄 License

Educational project — Holberton School.

## 👥 Author

Anne-Cécile Colléter
