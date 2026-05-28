import pytest
from app import db
from app.database.models import Project


class TestE2E:

    def test_get_projects_page(self, app, client):
        response = client.get('/proyectos')
        assert response.status_code in (302, 401)

    def test_get_clients_page(self, app, client):
        response = client.get('/clientes')
        assert response.status_code in (302, 401)

    def test_get_login_page(self, app, client):
        response = client.get('/login')
        assert response.status_code == 200
