import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app


@pytest.mark.asyncio
async def test_create_shop_admin_success():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            response = await ac.post("/admin/shop-admins", json={
                "username": "unit_admin",
                "password": "unitpass123",
                "email": "unitadmin@example.com",
                "role": "manager",
                "notes": "Unit test shop admin"
            })
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "unit_admin"
            assert data["role"] == "manager"
            assert "admin_id" in data



@pytest.mark.asyncio
async def test_create_shop_admin_invalid_role():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            response = await ac.post("/admin/shop-admins", json={
                "username": "bad_admin",
                "password": "testpass123",
                "email": "badadmin@example.com",
                "role": "invalid_role",
                "notes": "This should fail"
            })
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid role"


