from fastapi import APIRouter, HTTPException, Query, Request
from app.db import database
from sqlalchemy import update
from app.models import product 
from app.models import activity_log
from app.models import store_promotion
from app.models.user import users as user_table
from uuid import UUID

from sqlalchemy import update
from sqlalchemy import delete

from app.schemas.store_promotion import StorePromotionCreate, StorePromotionUpdate
from app.schemas.user import UserStatusUpdate
from app.models import user as user_model

from slowapi.errors import RateLimitExceeded

from fastapi.responses import JSONResponse

from app.extensions.limiter import limiter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.put("/product-category/{product_id}")
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def update_product_category(request:Request,product_id: str, new_category: str):
    query = (
        update(product.products)
        .where(product.products.c.product_id == product_id)
        .values(category=new_category)
        .returning(product.products.c.product_id, product.products.c.category)
    )
    result = await database.fetch_one(query)
    if result:
        return {"message": f"Product {result['product_id']} category updated to {result['category']}"}
    raise HTTPException(status_code=404, detail="Product not found")



@router.get("/activity-logs", summary="Retrieve user activity logs", description="Get a list of user activities for monitoring purposes.", tags=["Admin Panel"])
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def get_activity_logs(request:Request,limit: int = Query(10, le=100), offset: int = 0):

    query = activity_log.cms_activity_logs.select().limit(limit).offset(offset)
    results = await database.fetch_all(query)
    if results:
        return [{"log_id": str(r["log_id"]), "user_id": str(r["user_id"]), "activity_type": r["activity_type"], "payload": r["payload"], "timestamp": r["timestamp"]} for r in results]
    return {"message": "No activity logs found"}



# Create promotion
@router.post("/promotions", summary="Create a new promotion", description="Create a new store promotion with details like title, discount, start and end dates.", tags=["Admin Panel"])
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def create_promotion(request:Request,promotion: StorePromotionCreate):
    query = store_promotion.store_promotions.insert().values(**promotion.dict())
    await database.execute(query)
    return {"message": "Promotion created successfully."}


# Read promotions
@router.get("/promotions", summary="Get all promotions", description="Retrieve a list of all store promotions.", tags=["Admin Panel"])
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def get_promotions(request:Request):
    query = store_promotion.store_promotions.select()
    return await database.fetch_all(query)

# Update promotion
@router.put("/promotions/{promotion_id}", summary="Update a promotion", description="Update details of a specific store promotion by promotion ID.", tags=["Admin Panel"])
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def update_promotion(request:Request,promotion_id: UUID, update_data: StorePromotionUpdate):
    update_values = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_values:
        raise HTTPException(status_code=400, detail="No update data provided.")
    query = (
        store_promotion.store_promotions.update()
        .where(store_promotion.store_promotions.c.promotion_id == promotion_id)
        .values(**update_values)
        .returning(store_promotion.store_promotions.c.promotion_id)
    )
    result = await database.fetch_one(query)
    if result:
        return {"message": "Promotion updated successfully."}
    raise HTTPException(status_code=404, detail="Promotion not found.")



# Delete promotion
@router.delete("/promotions/{promotion_id}", summary="Delete a promotion", description="Delete a specific store promotion by promotion ID.", tags=["Admin Panel"])
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def delete_promotion(request:Request,promotion_id: UUID):
    query = (
        store_promotion.store_promotions.delete()
        .where(store_promotion.store_promotions.c.promotion_id == promotion_id)
        .returning(store_promotion.store_promotions.c.promotion_id)
    )
    result = await database.fetch_one(query)
    if result:
        return {"message": "Promotion deleted successfully."}
    raise HTTPException(status_code=404, detail="Promotion not found.")

@router.put("/user-status", summary="Update user status", description="Mall admin can ban, restrict, or activate users.", tags=["Admin Panel"])
@limiter.limit("3/minute")  # 3 requests per minute per IP
async def update_user_status(request:Request,update_data: UserStatusUpdate):
    query = (
        user_table.update()
        .where(user_table.c.id == update_data.user_id)
        .values(status=update_data.new_status)
        .returning(user_table.c.id)
    )
    result = await database.fetch_one(query)
    if result:
        return {"message": f"User status updated to {update_data.new_status}"}
    raise HTTPException(status_code=404, detail="User not found.")