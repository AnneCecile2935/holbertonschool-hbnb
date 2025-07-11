CREATE DATABASE IF NOT EXISTS hbnb;
use hbnb;

CREATE TABLE IF NOT EXISTS User(
	id CHAR(36) PRIMARY KEY,
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	email VARCHAR(255) UNIQUE NOT NULL, -- vérfiie l'unicité de l'email
	password VARCHAR(255) NOT NULL, -- est obligatoire
	is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place
(
	id CHAR(36) PRIMARY KEY,
	title VARCHAR(255),
	description TEXT, -- pas de limite de taille
	price DECIMAL(10, 2), -- deux chiffres après la virgule
	latitude FLOAT,
	longitude FLOAT,
	owner_id CHAR(36),
	FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE -- si user est delete, places sont delete
);

CREATE TABLE IF NOT EXISTS Review
(
	id CHAR(36) PRIMARY KEY,
	text TEXT,
	rating INT CHECK(rating >=1 AND rating <= 5),
	user_id CHAR(36),
	place_id CHAR(36),
	FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE CASCADE, -- lien avec table user
	FOREIGN KEY(place_id) REFERENCES Place(id) ON DELETE CASCADE, -- lien avec la table place
	UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity
(
	id CHAR(36) PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL -- equipement doit être unique
);

CREATE TABLE IF NOT EXISTS Place_Amenity
(
	place_id CHAR(36),
	amenity_id CHAR(36),
	PRIMARY KEY (place_id, amenity_id), -- empeche les doublons par place
	FOREIGN KEY(place_id) REFERENCES Place(id),
	FOREIGN KEY(amenity_id) REFERENCES Amenity(id)
);

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$97b7Z9KZu6klLv93AMJPS.hd9RSn4dy/vMPeGF0PZPYQjdzPqQOwO',
	TRUE
);

INSERT INTO Amenity (id, name) VALUES
('a1f50467-7f70-4a18-9be1-7b3472b55dc2', 'WiFi'),
('a2a0f2dd-38d2-420a-a5fd-6dc0503c9ea2', 'Swimming Pool'),
('a3bfb285-7751-4ae4-b56f-e5de58fa69e7', 'Air Conditioning');
