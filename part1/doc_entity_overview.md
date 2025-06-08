# 🛠️ Architecture – Entity Overview (Part 1 – Task 3)

## 🎯 Objectif

Ce document clôture la Partie 1 du projet HBnB en synthétisant l’organisation de nos entités principales, leur rôle fonctionnel, et leur articulation logique dans le système.

Il s’appuie sur les travaux réalisés lors des tâches précédentes :
- le diagramme de package UML (Tâche 0),
- le diagramme de classes UML (Tâche 1),
- les diagrammes de séquence (Tâche 2).

Notre objectif est ici de :
- décrire les entités clés de l'application,
- expliquer leurs relations structurelles,
- faire le lien avec les cas d’usage déjà modélisés,
- et anticiper leur implémentation dans le futur code.

---
## 🧱 Entités principales du système

| Entité     | Attributs clés                                      | Rôle métier                                                                 | Utilisation dans les cas d’usage |
|------------|------------------------------------------------------|------------------------------------------------------------------------------|----------------------------------|
| `BaseModel`| `id`, `create_instance`, `update_instance`           | Classe mère assurant l’unicité et la traçabilité des entités                | Inhérente à toutes les entités |
| `User`     | `id`, `name`, `surname`, `email`, `password`, `admin` | Représente un utilisateur de la plateforme (client ou administrateur)       | Créer un utilisateur, Créer une review, Créer un lieu |
| `Place`    | `id`, `title`, `description`, `price`, `latitude`, `longitude`, `user_id`, `review_ids` | Représente un lieu proposé par un utilisateur                               | Créer un lieu, Créer une review, Lister les lieux |
| `Review`   | `id`, `user_id`, `place_id`, `text`                   | Permet à un utilisateur de donner un avis sur un lieu                       | Créer une review |
| `Amenity`  | `id`, `name`                                          | Désigne un équipement ou service disponible dans un lieu                    | Permet de filtrer les lieux |

🧠 Remarques :
- Amenity est bien dans le diagramme de classes, mais pas utilisé dans les cas d’usage de la Partie 1 → Son usage est prévu pour plus tard.

---
## 🔗 Relations entre les entités

Nos entités sont liées entre elles selon une logique simple, reflétée dans notre diagramme de classes UML.

| Relation                       | Type de lien      | Détail technique / Implémentation |
|--------------------------------|-------------------|------------------------------------|
| `User` → `Place`               | One-to-Many       | Un utilisateur peut créer plusieurs lieux (`Place.user_id`) |
| `User` → `Review`              | One-to-Many       | Un utilisateur peut créer plusieurs reviews (`Review.user_id`) |
| `Place` → `Review`             | One-to-Many       | Un lieu peut recevoir plusieurs reviews (`Review.place_id`) |
| `Place` → `Amenity`            | Many-to-Many      | Un lieu peut avoir plusieurs services, et un service peut être partagé |
| Toutes entités → `BaseModel`  | Héritage          | Chaque entité hérite de `BaseModel` (pour les champs `id`, `create_instance`, `update_instance`) |

---
🧠 Remarques :

- Les relations `One-to-Many` sont matérialisées par une **clé étrangère** côté “Many” (ex: `place_id` dans `Review`).
- La relation `Place` ↔ `Amenity` nécessite une **table d’association** (ex : `place_amenity`).

---
## 🔄 Entités et cas d’usage

Voici comment les entités principales sont mobilisées dans les cas d’usage modélisés dans nos diagrammes de séquence :

| Cas d’usage              | Entités impliquées                            | Rôle des entités |
|--------------------------|-----------------------------------------------|------------------|
| Créer un utilisateur     | `User`, `BaseModel`                          | Le système crée un nouvel utilisateur avec un identifiant unique. |
| Créer un lieu (`Place`)  | `Place`, `User`, `BaseModel`                 | Le lieu est lié à l’utilisateur créateur via `user_id`. |
| Créer une review         | `Review`, `User`, `Place`, `BaseModel`       | La review est liée à un utilisateur (auteur) et à un lieu. Les deux doivent exister. |
| Lister les lieux         | `Place`                                      | Le système récupère tous les lieux, éventuellement filtrés par `Amenity`. |

---

🧠 Remarques :

- Ces cas d’usage couvrent **les principales interactions du système** : création, relation entre entités, lecture conditionnelle.

---
## 🛠️ Projection dans le code

Nos entités seront implémentées sous forme de **classes Python**, organisées selon une approche orientée objet classique.

### 🧱 Structure commune (héritage)

Toutes les entités (`User`, `Place`, `Review`, `Amenity`) hériteront d’une **classe mère `BaseModel`**, qui contiendra :

- un identifiant unique (`id`)
- une date de création (`create_instance`)
- une date de mise à jour (`update_instance`)
- des méthodes utiles comme :
  - `__init__()` : initialisation
  - `__str__()` : affichage formaté
  - `save()` : mise à jour de `update_instance`

Cela permet de **centraliser les comportements communs** et de **faciliter les extensions futures** (sérialisation, sauvegarde, etc.).

---

### 🧩 Exemples d’implémentation (sans code)

| Classe    | Attributs spécifiques                                   | Méthodes envisagées              |
|-----------|---------------------------------------------------------|----------------------------------|
| `User`    | `name`, `surname`, `email`, `password`, `admin`         | `delete()`, `save()`, `__str__()` |
| `Place`   | `title`, `description`, `price`, `latitude`, `longitude`, `user_id`, `review_ids`, `amenities` | `save()`, `get_reviews()` |
| `Review`  | `user_id`, `place_id`, `text`                            | `save()`                         |
| `Amenity` | `name`                                                   | `save()`                         |

---

🧠 Remarques :

- Les attributs comme `user_id`, `place_id`, `review_ids` matérialisent les **liens entre entités**.
- Certains attributs (comme `amenity`) pourront être des **listes d’objets ou d’identifiants**.
- L’implémentation respectera la **séparation logique** entre données (attributs) et actions (méthodes), avec un usage progressif des bonnes pratiques orientées objet.

---

## ✅ Conclusion

Cette documentation synthétise notre compréhension de l’architecture orientée objet de l’application HBnB.

Elle met en lumière :
- les **entités principales** manipulées dans notre système,
- leurs **relations structurelles et fonctionnelles**,
- leur **rôle concret dans les cas d’usage métier** modélisés précédemment,
- et leur **projection technique** dans le futur code.

La partie 1 de conception pose les bases d’un développement structuré, cohérent et maintenable.  
Il facilitera la mise en œuvre des prochaines étapes du projet : implémentation des classes, sérialisation, routes API, et gestion de la persistance.
