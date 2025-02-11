# tests/test_urls.py
from fastapi.testclient import TestClient
from main import app
from core.config import settings

client = TestClient(app)

def test_create_shorten_url():
    request_data = {
        "original_url": "http://example.com",
        "visibility": "public"
    }

    response = client.post("/url/create", json=request_data)

    assert response.status_code == 200
    response_data = response.json()
    assert "short_url" in response_data
    assert response_data["short_url"].startswith(f"{settings.service_url}/")


def test_url_status():
    short_id = "abc123"
    
    response = client.get(f"/url/{short_id}/status", params={"full_info": True, "max_result": 5, "offset": 0})
    
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert "total_accesses" in data
    assert "accesses" in data