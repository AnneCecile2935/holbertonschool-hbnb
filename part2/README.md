# HBnB Flask REST API

## 🧩 Objectif du projet

Ce projet est une API REST modulaire pour l'application HBnB, développée en Flask et structurée selon une architecture en couches :

- **Présentation (API)** : Gestion des routes et de l’exposition des services.
- **Logique métier (Modèles & Services)** : Contient la logique fonctionnelle et les entités principales.
- **Persistance (In-Memory Repository)** : Gère le stockage temporaire des objets, en attendant l'intégration d'une base de données (Partie 3).

---

## 📁 Structure du projet

```bash
hbnb/
├── app/
│   ├── __init__.py             # Initialise l'application Flask
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py        #  Routes liées aux utilisateurs
│   │       ├── places.py       #  Routes liées aux lieux
│   │       ├── reviews.py      #  Routes liées aux avis
│   │       └── amenities.py    #  Routes liées aux commodités
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # Modèle utilisateur
│   │   ├── place.py            # Modèle lieu
│   │   ├── review.py           # Modèle avis
│   │   └── amenity.py          # Modèle commodité
│   ├── services/
│   │   ├── __init__.py         # Instancie le HBnBFacade
│   │   └── facade.py           # Pattern façade entre API, modèles, et persistance
│   └── persistence/
│       ├── __init__.py
│       └── repository.py       # Référentiel en mémoire (InMemoryRepository)
├── run.py                      # Point d’entrée de l'application Flask
├── config.py                   # Configuration de l’application
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation du projet
```

---

## ⚙️ Installation & Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/Helvlaska/holbertonschool-hbnb.git
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l’application

```bash
python run.py
```

Par défaut, l'application démarre sur :
```
http://127.0.0.1:5000/
```

## 🛠 Configuration

Le fichier config.py contient des classes de configuration :

Config : Configuration de base

DevelopmentConfig : Activation du mode debug par défaut

Vous pouvez définir la variable d’environnement SECRET_KEY pour sécuriser votre application.

## 🔧 Dépendances

Le fichier requirements.txt inclut :

```

flask
flask-restx
```

## 🚧 État du projet

✅ Structure en place
✅ Repository en mémoire fonctionnel
✅ Facade instanciée
🕓 Routes API à implémenter dans les prochaines étapes
🕓 Intégration base de données prévue en Partie 3

## 📄 Licence

Projet pédagogique — Holberton School.
