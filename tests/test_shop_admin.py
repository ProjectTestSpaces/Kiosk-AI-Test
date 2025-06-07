# import pytest
# from httpx import AsyncClient, ASGITransport
# from asgi_lifespan import LifespanManager
# from app.main import app
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# # @pytest.mark.asyncio
# # async def test_create_shop_admin():
# #     async with LifespanManager(app):
# #         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
# #             response = await ac.post("/admin/shop-admins", json={
# #                 "username": "testadmin",
# #                 "password": "testpass123",
# #                 "email": "testadmin@example.com",
# #                 "role": "manager",
# #                 "notes": "Integration test admin"
# #             })
# #             assert response.status_code == 200
# #             data = response.json()
# #             assert data["username"] == "testadmin"
# #             assert data["email"] == "testadmin@example.com"
# #             assert data["role"] == "manager"
# #             assert "admin_id" in data

# async def get_auth_headers(ac: AsyncClient) -> dict:
#     response = await ac.post("/auth/admin-login", json={
#         "username": "admin",
#         "password": "password"
#     })
#     assert response.status_code == 200
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}


# @pytest.mark.asyncio
# async def test_create_shop_admin():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             headers = await get_auth_headers(ac)
#             response = await ac.post("/admin/shop-admins", json={
#                 "username": "testadmin",
#                 "password": "testpass123",
#                 "email": "testadmin@example.com",
#                 "role": "manager",
#                 "notes": "Integration test admin"
#             }, headers=headers)
#             assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_create_shop_admin_invalid_role():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             response = await ac.post("/admin/shop-admins", json={
#                 "username": "badrole",
#                 "password": "testpass123",
#                 "email": "badrole@example.com",
#                 "role": "invalid_role",
#                 "notes": "Should fail"
#             })
#             assert response.status_code == 400
#             assert response.json()["detail"] == "Invalid role"


# @pytest.mark.asyncio
# async def test_get_shop_admins():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             response = await ac.get("/admin/shop-admins")
#             assert response.status_code == 200
#             assert isinstance(response.json(), list)


# @pytest.mark.asyncio
# async def test_update_shop_admin():
#     # First create one
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             create_resp = await ac.post("/admin/shop-admins", json={
#                 "username": "updatableadmin",
#                 "password": "testpass",
#                 "email": "updatable@example.com",
#                 "role": "viewer",
#                 "notes": "Initial"
#             })
#             admin_id = create_resp.json()["admin_id"]

#             # Now update role and status
#             update_resp = await ac.put(f"/admin/shop-admins/{admin_id}", json={
#                 "role": "manager",
#                 "status": "active"
#             })
#             assert update_resp.status_code == 200
#             assert update_resp.json()["message"] == "Shop admin updated successfully."



# @pytest.mark.asyncio
# async def test_delete_shop_admin():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             # Create first
#             create_resp = await ac.post("/admin/shop-admins", json={
#                 "username": "deletableadmin",
#                 "password": "testpass",
#                 "email": "deletable@example.com",
#                 "role": "staff"
#             })
#             admin_id = create_resp.json()["admin_id"]

#             # Then delete
#             delete_resp = await ac.delete(f"/admin/shop-admins/{admin_id}")
#             assert delete_resp.status_code == 200
#             assert delete_resp.json()["message"] == "Shop admin deleted successfully."

import pytest
import os
import sys
from uuid import uuid4
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app

# Ensure the app path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Helper to get JWT headers
async def get_auth_headers(ac: AsyncClient) -> dict:
    response = await ac.post("/auth/admin-login", json={
        "username": "admin",
        "password": "password"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_shop_admin():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            headers = await get_auth_headers(ac)
            unique = str(uuid4())[:8]
            response = await ac.post("/admin/shop-admins", json={
                "username": f"testadmin_{unique}",
                "password": "testpass123",
                "email": f"testadmin_{unique}@example.com",
                "role": "manager",
                "notes": "Integration test admin"
            }, headers=headers)
            assert response.status_code == 200
            data = response.json()
            assert data["username"].startswith("testadmin_")
            assert data["role"] == "manager"


@pytest.mark.asyncio
async def test_create_shop_admin_invalid_role():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            headers = await get_auth_headers(ac)
            response = await ac.post("/admin/shop-admins", json={
                "username": "badrole",
                "password": "testpass123",
                "email": "badrole@example.com",
                "role": "invalid_role",
                "notes": "Should fail"
            }, headers=headers)
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid role"


# @pytest.mark.asyncio
# async def test_get_shop_admins():
#     async with LifespanManager(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
#             headers = await get_auth_headers(ac)
#             response = await ac.get("/admin/shop-admins", headers=headers)
#             assert response.status_code == 200
#             assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_shop_admins():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            headers = await get_auth_headers(ac)
            response = await ac.get("/admin/shop-admins", headers=headers)
            print("GET /admin/shop-admins response:", response.status_code, response.json())
            assert response.status_code == 200
            assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_shop_admin():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            headers = await get_auth_headers(ac)

            # Create admin
            unique = str(uuid4())[:8]
            create_resp = await ac.post("/admin/shop-admins", json={
                "username": f"updateadmin_{unique}",
                "password": "testpass",
                "email": f"updateadmin_{unique}@example.com",
                "role": "viewer"
            }, headers=headers)
            admin_id = create_resp.json()["admin_id"]

            # Update role
            update_resp = await ac.put(f"/admin/shop-admins/{admin_id}", json={
                "role": "manager",
                "status": "active"
            }, headers=headers)
            assert update_resp.status_code == 200
            assert update_resp.json()["message"] == "Shop admin updated successfully."

from uuid import uuid4

@pytest.mark.asyncio
async def test_delete_shop_admin():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
            headers = await get_auth_headers(ac)

            # Create admin to delete
            unique = str(uuid4())[:8]
            create_resp = await ac.post("/admin/shop-admins", json={
                "username": f"deleteadmin_{unique}",
                "password": "testpass",
                "email": f"deleteadmin_{unique}@example.com",
                "role": "staff"
            }, headers=headers)

            # Debug output
            print("CREATE response status:", create_resp.status_code)
            print("CREATE response JSON:", create_resp.json())

            assert create_resp.status_code == 200
            data = create_resp.json()
            assert "admin_id" in data

            admin_id = data["admin_id"]

            # Then delete
            delete_resp = await ac.delete(f"/admin/shop-admins/{admin_id}", headers=headers)
            print("DELETE response:", delete_resp.status_code, delete_resp.json())

            assert delete_resp.status_code == 200
            assert delete_resp.json()["message"] == "Shop admin deleted successfully."
