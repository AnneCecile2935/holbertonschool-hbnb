# HBnB Flask REST API

## 🧩 Project Objective

This README presents the architecture and design of a simplified version of
an AirBnB-like application named HBnB Evolution.
The application allows users to perform the following primary operations:

User Management: Users can register, update their profiles,
and be identified as either regular users or administrators.

Place Management: Users can list properties (places) they own, specifying
 details such as name, description, price, and location (latitude and longitude). Each place can also have a list of amenities.

Review Management: Users can leave reviews for places they have visited,
including a rating and a comment.

Amenity Management: The application manages amenities that can be associated
with places.

---
## Project Architecture
The project follows a layered architecture:

Presentation Layer (API): Handles HTTP routes and service exposure.

Business Logic (Models & Services): Contains core functionality and main entities.

Persistence Layer (In-Memory Repository): Manages temporary storage of objects, with planned database integration in Part 3.
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
│   │   ├── __init__.py                 # Instantiates HBnBFacade
│   │   └── facade.py                   # Facade pattern between API, models, and persistence
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py               # In-memory repository (InMemoryRepository)
│   └── tests/                          # Unit tests
│       ├── __init__.py
│       ├── test_amenity.py             # Tests for Amenity model
│       ├── test_amenity_api.py         # API tests for Amenity
│       ├── test_base_model.py          # Tests for BaseModel
│       ├── test_place.py               # Tests for Place model
│       ├── test_place_api.py           # API tests for Place
│       ├── test_review.py              # Tests for Review model
│       ├── test_review_api.py          # API tests for Review
│       ├── test_user.py                # Tests for User model
│       ├── test_user_api.py            # API tests for User
├── run.py                              # Flask app entry point
├── config.py                           # Application configuration
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation

```

---


## Business Rules and Requirements

### User Entity
Attributes: first name, last name, email, and password.

Users can be identified as administrators via a boolean attribute.

Users can register, update their profile information, and be deleted.

### Place Entity
Attributes: title, description, price, latitude, and longitude.

Places are associated with the user who created (owns) them.

Places can have a list of amenities.

Places can be created, updated, deleted, and listed.

### Review Entity
Each review is associated with a specific place and user.

Includes a rating and comment.

Reviews can be created, updated, deleted, and listed by place.

### Amenity Entity
Attributes: name and description.

Amenities can be created, updated, deleted, and listed.

### General
Each entity is uniquely identified by an ID.

Creation and update datetime fields are recorded for auditing purposes.

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


## Entity Tests

### User

from app.models.user_model import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print(user.__dict__)
    print("User creation test passed!")

test_user_creation()

### Place and Relationships

from app.models.place_model import Place
from app.models.user_model import User
from app.models.review_model import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100,
                  latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Great stay!", rating=5, place=place, author=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()

### Amenity

from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()

## Author

Anne-Cécile Colléter
Claire Castan

## 📄 License

Educational project — Holberton School.
