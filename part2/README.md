# HBnB Flask REST API

## 🧩 Project Objective

This project is a modular REST API for the HBnB application,
developed using Flask and structured following a layered architecture:

- **Presentation Layer (API)** : Manages routes and service exposure.
- **Business Logic (Models & Services)** : Contains functional logic
and main entities.
- **Persistance (In-Memory Repository)** : Manages temporary storage of objects,
with a database integration planned in Part 3.

---

## 📁 Project Structure

```bash
hbnb/
├── app/
│   ├── __init__.py                     # Initialize the Flask application
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py                # User-related routes
│   │       ├── places.py               # Place-related routes
│   │       ├── reviews.py              # Review-related routes
│   │       └── amenities.py            # Amenity-related routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py               # BaseModel class
│   │   ├── user.py                     # User model
│   │   ├── place.py                    # Place model
│   │   ├── review.py                   # Review model
│   │   └── amenity.py                  # Amenity model
│   ├── services/
│   │   ├── __init__.py                 # Instantiates the HBnBFacade
│   │   └── facade.py                   # Facade pattern between API, models, and persistence
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py               # In-memory repository (InMemoryRepository)
│   └── tests/                         # Unit tests
│       ├── __init__.py
│       ├── test_base_model.py          # Tests for BaseModel
│       ├── test_user.py                # Tests for User
│       ├── test_place.py               # Tests for Place
│       ├── test_review.py              # Tests for Review
│       └── test_amenity.py             # Tests for Amenity
├── run.py                            # Flask app entry point
├── config.py                         # Application configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## ⚙️  Installation & Running

### 1. Clone the repository

```bash
git clone https://github.com/Helvlaska/holbertonschool-hbnb.git
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4.  Start the application

```bash
python run.py
```

By default, the app will be available at:
```
http://127.0.0.1:5000/
```

## 🛠 Configuration

The config.py file includes configuration classes:

Config: Base configuration

DevelopmentConfig: Debug mode enabled by default

You can set the SECRET_KEY environment variable to secure your application.

## 🔧 Dependencies

The requirements.txt file includes:

```

flask
flask-restx
```

## 🚧 Project Status

✅ Project structure in place
✅ Functional in-memory repository
✅ Facade instantiated
🕓 API routes to be implemented in upcoming steps
🕓 Database integration planned for Part 3

## 📄 License

Educational project — Holberton School.
