import pytest
import httpx
from httpx import AsyncClient
from app.main import app
from asgi_lifespan import LifespanManager

@pytest.mark.asyncio
async def test_admin_login_success():
    async with LifespanManager(app):
        # Fix: Use the newer httpx.AsyncClient API with transport
        async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as ac:
            response = await ac.post("/auth/admin-login", json={"username": "admin", "password": "password"})
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"