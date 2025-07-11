-- ============================
-- Tests CRUD
-- ============================

-- 1. User
-- CREATE (donnée temporaire)
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$examplehashedpasswordjohn',
    FALSE
);

-- READ
SELECT * FROM User;

-- UPDATE
UPDATE User
SET first_name = 'Johnny'
WHERE id = '11111111-1111-1111-1111-111111111111';

-- DELETE (donnée temporaire)
DELETE FROM User
WHERE id = '11111111-1111-1111-1111-111111111111';

-- 2. Place
-- CREATE (donnée temporaire)
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Cozy Studio',
    'A quiet place to stay',
    89.99,
    48.8566,
    2.3522,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- READ
SELECT * FROM Place;

-- UPDATE
UPDATE Place
SET price = 95.00
WHERE id = '22222222-2222-2222-2222-222222222222';

-- DELETE (donnée temporaire)
DELETE FROM Place
WHERE id = '22222222-2222-2222-2222-222222222222';

-- 3. Amenity
-- CREATE (donnée temporaire)
INSERT INTO Amenity (id, name)
VALUES ('33333333-3333-3333-3333-333333333333', 'Jacuzzi');

-- READ
SELECT * FROM Amenity;

-- UPDATE
UPDATE Amenity
SET name = 'Outdoor Jacuzzi'
WHERE id = '33333333-3333-3333-3333-333333333333';

-- DELETE (donnée temporaire)
DELETE FROM Amenity
WHERE id = '33333333-3333-3333-3333-333333333333';

-- 4. Place_Amenity
-- CREATE (relation temporaire)
-- Attention : il faut que la place et l'amenity existent au moment de l'insertion
-- On réinsère place et amenity temporaire pour assurer la FK
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    'Temporary Place',
    'Temporary description',
    50.00,
    40.7128,
    -74.0060,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

INSERT INTO Amenity (id, name)
VALUES ('55555555-5555-5555-5555-555555555555', 'Temporary Amenity');

INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    '55555555-5555-5555-5555-555555555555'
);

-- READ
SELECT * FROM Place_Amenity;

-- DELETE (relation temporaire)
DELETE FROM Place_Amenity
WHERE place_id = '44444444-4444-4444-4444-444444444444'
AND amenity_id = '55555555-5555-5555-5555-555555555555';

-- Nettoyage des données temporaires utilisées pour relation
DELETE FROM Place
WHERE id = '44444444-4444-4444-4444-444444444444';

DELETE FROM Amenity
WHERE id = '55555555-5555-5555-5555-555555555555';

-- 5. Review
-- CREATE (donnée temporaire)
-- La place et l'user doivent exister pour respecter les FK
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '66666666-6666-6666-6666-666666666666',
    'Review Place',
    'Place for review test',
    75.00,
    34.0522,
    -118.2437,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '77777777-7777-7777-7777-777777777777',
    'Review',
    'User',
    'review.user@example.com',
    '$2b$12$examplehashedpasswordreview',
    FALSE
);

INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES (
    '88888888-8888-8888-8888-888888888888',
    'Great location and clean space.',
    5,
    '77777777-7777-7777-7777-777777777777',
    '66666666-6666-6666-6666-666666666666'
);

-- READ
SELECT * FROM Review;

-- UPD
