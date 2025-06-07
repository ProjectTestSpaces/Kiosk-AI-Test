from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from databases import Database
from app.db import database
from app.models import shop_admin as shop_admin_model
from app.schemas import shop_admin as shop_admin_schema
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

# Create shop admin
@router.post("/shop-admins", response_model=shop_admin_schema.ShopAdminOut)
async def create_shop_admin(admin: shop_admin_schema.ShopAdminCreate):
    if admin.role not in ["manager", "staff", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    new_admin_id = uuid4()
    query = shop_admin_model.shop_admins.insert().values(
        admin_id=new_admin_id,
        **admin.dict()
    )
    await database.execute(query)

    return {
        "admin_id": new_admin_id,
        **admin.dict(),
        "status": "active",
        "created_at": datetime.utcnow()  # temporary stub; accurate time needs DB fetch
    }
# Get all shop admins
@router.get("/shop-admins", response_model=list[shop_admin_schema.ShopAdminOut])
async def list_shop_admins():
    query = shop_admin_model.shop_admins.select()
    results = await database.fetch_all(query)
    return results

# Update shop admin role/status
@router.put("/shop-admins/{admin_id}")
async def update_shop_admin(admin_id: UUID, update: shop_admin_schema.ShopAdminUpdate):
    update_values = {k: v for k, v in update.dict().items() if v is not None}
    if not update_values:
        raise HTTPException(status_code=400, detail="No update data provided.")

    query = shop_admin_model.shop_admins.update().where(
        shop_admin_model.shop_admins.c.admin_id == admin_id
    ).values(**update_values)
    result = await database.execute(query)
    if result:
        return {"message": "Shop admin updated successfully."}
    raise HTTPException(status_code=404, detail="Shop admin not found.")

# Delete shop admin
@router.delete("/shop-admins/{admin_id}")
async def delete_shop_admin(admin_id: UUID):
    query = shop_admin_model.shop_admins.delete().where(
        shop_admin_model.shop_admins.c.admin_id == admin_id
    )
    print("This is Query>>",query)

    result = await database.execute(query)
    print("This is result>>",result)
    if result:
        return {"message": "Shop admin deleted successfully."}
    raise HTTPException(status_code=404, detail="Shop admin not found.")
