from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404

def test_get_users_by_category():
    response = client.get("/users/?categoria=admin")
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_obtener_peliculas():
    response = client.get("/peliculas")
    assert response.status_code == 200
    assert "mensaje" in response.json()[0]

def test_obtener_pelicula():
    response = client.get("/peliculas/1")
    assert response.status_code == 200
    assert "mensaje" in response.json()[0]

def test_obtener_pelicula_por_categoria():
    response = client.get("/peliculas/?categoria=accion")
    assert response.status_code == 200
    assert "mensaje" in response.json()[0]