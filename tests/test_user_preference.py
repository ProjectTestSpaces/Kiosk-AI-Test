

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from asgi_lifespan import LifespanManager


# Ensure the app path is in sys.path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



@pytest.mark.asyncio
async def test_user_preference_update():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            response = await ac.post("/user-preference/update", json={
                "user_id": "111e4567-e89b-12d3-a456-426614174000",
                "preference_key": "theme",
                "preference_value": "dark"
            })
            assert response.status_code == 200
            assert "updated" in response.json()["message"].lower()
