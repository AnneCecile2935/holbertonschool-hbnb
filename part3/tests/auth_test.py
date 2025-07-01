import pytest
from app import create_app, db
from app.models import User
from flask_jwt_extended import decode_token

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_login_issues_jwt(client):
    # Création d’un utilisateur test
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    # Requête POST vers le login
    response = client.post('/login', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

    # Vérification que le token est un JWT valide
    token = data['access_token']
    decoded = decode_token(token)
    assert decoded['identity'] == user.id

def test_protected_endpoint_requires_jwt(client):
    # Appel sans JWT
    response = client.get('/protected-endpoint')
    assert response.status_code == 401  # Unauthorized

def test_protected_endpoint_with_valid_jwt(client):
    # Création utilisateur et génération token
    user = User(username='user1')
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()

    login_resp = client.post('/login', json={'username': 'user1', 'password': 'pass'})
    token = login_resp.get_json()['access_token']

    # Accès avec token
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/protected-endpoint', headers=headers)
    assert response.status_code == 200

def test_admin_endpoint_access(client):
    # Utilisateur non admin
    user = User(username='user2', is_admin=False)
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()

    login_resp = client.post('/login', json={'username': 'user2', 'password': 'pass'})
    token = login_resp.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/admin-only-endpoint', headers=headers)
    assert response.status_code == 403  # Forbidden

def test_admin_endpoint_access_with_admin(client):
    # Utilisateur admin
    admin = User(username='admin', is_admin=True)
    admin.set_password('adminpass')
    db.session.add(admin)
    db.session.commit()

    login_resp = client.post('/login', json={'username': 'admin', 'password': 'adminpass'})
    token = login_resp.get_json()['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/admin-only-endpoint', headers=headers)
    assert response.status_code == 200
