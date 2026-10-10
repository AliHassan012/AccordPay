from fastapi.testclient import TestClient
from app import app

def test_local_health_and_setup_screen():
    with TestClient(app) as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json()['demo_funds_only'] is True
        home = client.get('/')
        assert home.status_code == 200
        assert 'AccordPay' in home.text
        assert 'DEMO FUNDS' in home.text
