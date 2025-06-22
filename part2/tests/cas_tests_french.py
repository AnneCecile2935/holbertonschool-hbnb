# 🧪 Documentation du processus de test – Endpoints : User, Place, Review, Amenity

## 1. Objectif

Vérifier le bon fonctionnement des endpoints de l’API liés aux entités suivantes :
- `User` : gestion des utilisateurs
- `Place` : gestion des lieux
- `Review` : avis laissés par les utilisateurs
- `Amenity` : équipements disponibles dans un lieu

Chaque test couvre :
- Les cas d’usage standards (CRUD)
- Les cas limites / erreurs
- Les règles métier (validation, cohérence des données)

---

## 2. Environnement de test

| Élément            | Outil / Version         |
|--------------------|-------------------------|
| Framework API      | Flask + Flask-RESTx     |
| Outils de test     | Swagger UI, Postman     |
| Base de données    | SQLite (test locale)    |
| Méthode de test    | Appels manuels / automatisés |
| Version du code    | Commit `v1.0` (branche `dev`) |

---

## 3. Cas de test par entité

### 🧑‍💼 User

| ID   | Scénario                                 | Entrée / Requête                    | Résultat attendu            | Statut |
|------|------------------------------------------|-------------------------------------|------------------------------|--------|
| U01  | Création d’un utilisateur valide         | `POST /users` + JSON complet        | 201 Created + JSON user      | ✅     |
| U02  | Création avec email déjà utilisé         | Même email qu’un utilisateur existant | 400 Bad Request             | ✅     |
| U03  | Récupération utilisateur existant        | `GET /users/<user_id>`              | 200 OK + JSON user           | ✅     |
| U04  | Récupération utilisateur inexistant      | `GET /users/<fake_id>`              | 404 Not Found                | ✅     |

---

### 🏠 Place

| ID   | Scénario                                | Requête                             | Résultat attendu             | Statut |
|------|-----------------------------------------|-------------------------------------|-------------------------------|--------|
| P01  | Création d’un lieu avec `owner` valide  | `POST /places` + JSON               | 201 Created + lieu            | ✅     |
| P02  | Création sans `owner`                   | JSON sans champ `owner`             | 400 Bad Request               | ✅     |
| P03  | Création avec `owner` inexistant        | `owner = "invalid-id"`              | 404 Not Found                 | ✅     |
| P04  | Récupération d’un lieu                  | `GET /places/<id>`                  | 200 OK                        | ✅     |
| P05  | Modification d’un lieu (sans owner)     | `PUT /places/<id>` + update data    | 200 OK                        | ✅     |
| P06  | Tentative de modification du `owner`    | `PUT` contenant `owner`             | 400 Bad Request (rejeté)      | ✅     |

---

### ✍️ Review

| ID   | Scénario                                  | Requête                              | Résultat attendu             | Statut |
|------|-------------------------------------------|--------------------------------------|-------------------------------|--------|
| R01  | Création d’une review valide              | `POST /reviews` + JSON complet       | 201 Created                   | ✅     |
| R02  | Création avec `rating` hors bornes        | `rating = 6`                         | 400 Bad Request               | ✅     |
| R03  | Création avec champ manquant              | JSON sans `text`                     | 400 Bad Request               | ✅     |
| R04  | Récupération d’une review existante       | `GET /reviews/<id>`                  | 200 OK                        | ✅     |
| R05  | Récupération des reviews d’un lieu        | `GET /reviews/places/<place_id>`     | 200 OK + liste                | ✅     |
| R06  | Mise à jour d’une review (rating & text)  | `PUT /reviews/<id>` + valid payload  | 200 OK                        | ✅     |

---

### 🛠️ Amenity

| ID   | Scénario                                    | Requête                             | Résultat attendu             | Statut |
|------|---------------------------------------------|-------------------------------------|-------------------------------|--------|
| A01  | Création d’un amenity valide                | `POST /amenities` + JSON            | 201 Created                   | ✅     |
| A02  | Création avec champ `name` manquant         | JSON sans `name`                    | 400 Bad Request               | ✅     |
| A03  | Récupération d’un amenity                   | `GET /amenities/<id>`               | 200 OK                        | ✅     |
| A04  | Lister tous les amenities                   | `GET /amenities`                    | 200 OK + liste                | ✅     |
| A05  | Suppression d’un amenity                    | `DELETE /amenities/<id>`            | 204 No Content                | ✅     |
| A06  | Lien entre Amenity et Place (si applicable) | `GET /places/<id>/amenities`        | 200 OK                        | ✅     |

---

## 4. Résumé de couverture

| Entité   | Création | Lecture (GET) | Mise à jour (PUT) | Suppression (DELETE) | Validation métier |
|----------|----------|----------------|-------------------|------------------------|--------------------|
| User     | ✅        | ✅              | –                 | –                      | ✅ (email unique)  |
| Place    | ✅        | ✅              | ✅                 | –                      | ✅ (owner requis)  |
| Review   | ✅        | ✅              | ✅                 | –                      | ✅ (note valide)   |
| Amenity  | ✅        | ✅              | –                 | ✅                     | ✅ (`name` requis) |

---

## 5. Améliorations futures recommandées

- 🔐 Intégration de tests d'autorisation (ex. : seuls les propriétaires peuvent modifier un lieu)
- ⚙️ Intégration dans une suite `pytest` automatisée
- 📊 Tests de performance pour évaluer le comportement sous forte charge
- 🧪 Mocking des couches `facade` et `repository` pour des tests unitaires précis

---
