# 🏠 HBnB – Educational Project Inspired by Airbnb

Welcome to the **HBnB** project repository, a modular web application inspired
by Airbnb, developed step-by-step in an educational context.

This project demonstrates best practices in software design, UML modeling,
back-end API development, and will progressively extend to front-end features
and database integration.

---

## 🎯 Project Goals

- Design a **clear and modular architecture**
- **Model and implement** business entities (`User`, `Place`, `Review`, `Amenity`)
- Develop a **REST API** for data management
- Gradually extend the project with **additional technical layers**

---

## 🔧 Technologies (progressively introduced)

- Python
- UML (Mermaid.js)
- SQL (upcoming)
- REST API
- Front-end (upcoming)


---

## 🧱 Current Repository Structure

```bash
Holbertonschool-hbnb/Part1
├── README.md
├── part1/
│   ├── package_diagram.md
│   ├── class_diagram.md
│   ├── seq_diag_create_user.md
│   ├── seq_diag_create_place.md
│   ├── seq_diag_create_review.md
│   ├── seq_diag_list_place.md
│   ├── doc_entity_overview.md
│   └── README.md
├── docs/
│   ├── doc_package_diagram.md
│   ├── doc_class_diagram.md
│   ├── doc_sequence_diagram.md
│   ├── doc_sequence_diagram_detailed.md
```


---


```bash
Holbertonschool-hbnb/Part2
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

## 📌 Part 1 – Design (Technical Design & Modeling)

The first phase focused on defining the system’s foundation without writing code.
The goal was to **model the overall application workflow** through:

- **Package diagrams**: modular organization of components
- **Class diagrams**: definition of entities and relationships
- **Sequence diagrams**: use cases (creating a place, a user, a review, etc.)
- **Textual documentation**: descriptions of entities and business rules

🧰 *Tools used*: UML, Mermaid.js, Markdown

👉 See: `part1/` and `docs/`

---

## ⚙️ Part 2 – Business Logic & API Development

The second phase involves **implementing business entities** and
**exposing a REST API** to interact with them.

### ✅ Implemented features:

- Create, retrieve and update:
  - **users**, **places**, **amenities**, **reviews**
- Delete **reviews**
- Manage relationships:
  - a user owns multiple places and reviews
  - a place can have multiple amenities
- Enriched serialization, e.g., including owner name in place data

### 🧱 Technical architecture:

- 3-tier architecture:
  - Presentation: API (Flask + Flask-Restx)
  - Business logic: Services / Facade
  - Persistence (temporary): In-Memory Repository
- Use of the **Facade design pattern**
- Manual testing (via `curl`, Swagger) and automated tests (`unittest`)

🛠 *Technologies used*: Python 3, Flask, Flask-Restx

👉 See: `part2/`

---

## 🧠 What We Learned

### Part 1: Design Phase
- How to model a clear and modular architecture using UML diagrams.
- How to define and describe core business entities and their relationships.
- The importance of planning with use cases and sequence diagrams to visualize system interactions.
- Setting a solid foundation that guides future development phases.

### Part 2: Implementation of Business Logic and API Endpoints
- How to translate designs into modular, maintainable Python code using OOP principles.
- Building the Business Logic layer with core models like User, Place, Review, and Amenity.
- Creating RESTful API endpoints using Flask and flask-restx for clear and scalable communication.
- Implementing data serialization and handling relationships between entities.
- Testing and validating API functionality to ensure reliability and correctness.

Together, these parts helped us develop practical skills in software design and API development, creating a robust base for the HBnB project’s upcoming stages.

## 🚧 Upcoming Work

Future phases (Parts 3 & 4) will include:

- 📦 **Integration of an SQL database** (SQLAlchemy or custom ORM)
- 🧪 **Extended automated testing**
- 🖼 **Front-end development** (HTML/JS or modern framework)
- 🔐 **Authentication and session management**
- 🧩 **Progressive deployment on servers or containers**

---

## 👩‍💻 Authors

- Anne-Cécile Colléter
- Claire Castan

---

## 📄 License

Educational project — Holberton School.

---
