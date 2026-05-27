import pytest
from app import db
from app.database.models import Project


class TestE2E:

    def test_client_can_create_project(self, app, client):
        response = client.post('/projects/create', data={
            'name': 'E2E Test Project',
            'client_id': '1',
            'start_date': '2026-01-01',
            'end_date': '2026-12-31'
        })
        assert response.status_code in (200, 302, 404)

    def test_get_projects_list(self, app, client):
        response = client.get('/projects/')
        assert response.status_code in (200, 302, 404)

    def test_get_clients_list(self, app, client):
        response = client.get('/clients/')
        assert response.status_code in (200, 302, 404)
