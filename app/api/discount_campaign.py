from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from app.db import database
from app.models import discount_campaigns as dc_model


from app.schemas.discount_campaign import (
    DiscountCampaignCreate,
    DiscountCampaignUpdate,
    DiscountCampaignOut,
)
from uuid import UUID
from datetime import date
from sqlalchemy import select, and_
from app.api.auth import get_current_admin_user
from app.middleware.rbac import require_role

router = APIRouter(
    prefix="/admin/discount-campaigns",
    tags=["Discount Campaigns"],
    dependencies=[Depends(get_current_admin_user), Depends(require_role("mall_admin"))],
)

# Create
# @router.post("/", response_model=DiscountCampaignOut)
# async def create_campaign(payload: DiscountCampaignCreate):
#     if payload.end_date < payload.start_date:
#         raise HTTPException(status_code=400, detail="End date cannot be before start date")

#     query = dc_model.discount_campaigns.insert().values(**payload.dict())
#     campaign_id = await database.execute(query)

#     result = await database.fetch_one(
#         dc_model.discount_campaigns.select().where(dc_model.discount_campaigns.c.campaign_id == campaign_id)
#     )
#     return result


@router.post("/", response_model=DiscountCampaignOut)
async def create_campaign(payload: DiscountCampaignCreate):
    try:
        if payload.end_date < payload.start_date:
            raise HTTPException(status_code=400, detail="End date cannot be before start date")

        query = dc_model.discount_campaigns.insert().values(**payload.dict())
        campaign_id = await database.execute(query)

        result = await database.fetch_one(
            dc_model.discount_campaigns.select().where(dc_model.discount_campaigns.c.campaign_id == campaign_id)
        )
        return result
    
    except Exception as e:
        print(f"Exception in create_campaign: {type(e).__name__}: {str(e)}")
        print(f"Exception details: {repr(e)}")
        import traceback
        traceback.print_exc()
        raise

# Read with pagination
@router.get("/", response_model=list[DiscountCampaignOut])
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    shop_id: Optional[UUID] = None,
    status: Optional[str] = Query(None, pattern="^(active|expired|cancelled)$"),
):
    query = select(dc_model.discount_campaigns)
    if shop_id:
        query = query.where(dc_model.discount_campaigns.c.shop_id == shop_id)
    if status:
        query = query.where(dc_model.discount_campaigns.c.status == status)
    query = query.offset(skip).limit(limit)

    return await database.fetch_all(query)


# Update
@router.put("/{campaign_id}", response_model=dict)
async def update_campaign(campaign_id: UUID, payload: DiscountCampaignUpdate):
    if payload.start_date and payload.end_date and payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    query = (
        dc_model.discount_campaigns.update()
        .where(dc_model.discount_campaigns.c.campaign_id == campaign_id)
        .values(**update_data)
        .returning(dc_model.discount_campaigns.c.campaign_id)
    )
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign updated successfully"}


# Delete
@router.delete("/{campaign_id}", response_model=dict)
async def delete_campaign(campaign_id: UUID):
    query = (
        dc_model.discount_campaigns.delete()
        .where(dc_model.discount_campaigns.c.campaign_id == campaign_id)
        .returning(dc_model.discount_campaigns.c.campaign_id)
    )
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}



# from typing import Optional
# from fastapi import APIRouter, HTTPException, Depends, Query
# from app.db import database
# from app.models.discount_campaigns import discount_campaigns  # Import the table directly

# from app.schemas.discount_campaign import (
#     DiscountCampaignCreate,
#     DiscountCampaignUpdate,
#     DiscountCampaignOut,
# )
# from uuid import UUID
# from datetime import date
# from sqlalchemy import select, and_
# from app.api.auth import get_current_admin_user
# from app.middleware.rbac import require_role

# router = APIRouter(
#     prefix="/admin/discount-campaigns",
#     tags=["Discount Campaigns"],
#     dependencies=[Depends(get_current_admin_user), Depends(require_role("mall_admin"))],
# )

# # Create
# @router.post("/", response_model=DiscountCampaignOut)
# async def create_campaign(payload: DiscountCampaignCreate):
#     if payload.end_date < payload.start_date:
#         raise HTTPException(status_code=400, detail="End date cannot be before start date")

#     query = discount_campaigns.insert().values(**payload.dict())
#     campaign_id = await database.execute(query)

#     result = await database.fetch_one(
#         discount_campaigns.select().where(discount_campaigns.c.campaign_id == campaign_id)
#     )
#     return result


# # Read with pagination
# @router.get("/", response_model=list[DiscountCampaignOut])
# async def get_campaigns(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(10, le=100),
#     shop_id: Optional[UUID] = None,
#     status: Optional[str] = Query(None, pattern="^(active|expired|cancelled)$"),
# ):
#     query = select(discount_campaigns)
#     if shop_id:
#         query = query.where(discount_campaigns.c.shop_id == shop_id)
#     if status:
#         query = query.where(discount_campaigns.c.status == status)
#     query = query.offset(skip).limit(limit)

#     return await database.fetch_all(query)


# # Update
# @router.put("/{campaign_id}", response_model=dict)
# async def update_campaign(campaign_id: UUID, payload: DiscountCampaignUpdate):
#     if payload.start_date and payload.end_date and payload.end_date < payload.start_date:
#         raise HTTPException(status_code=400, detail="End date cannot be before start date")

#     update_data = {k: v for k, v in payload.dict().items() if v is not None}
#     if not update_data:
#         raise HTTPException(status_code=400, detail="No fields to update")

#     query = (
#         discount_campaigns.update()
#         .where(discount_campaigns.c.campaign_id == campaign_id)
#         .values(**update_data)
#         .returning(discount_campaigns.c.campaign_id)
#     )
#     result = await database.fetch_one(query)
#     if not result:
#         raise HTTPException(status_code=404, detail="Campaign not found")
#     return {"message": "Campaign updated successfully"}


# # Delete
# @router.delete("/{campaign_id}", response_model=dict)
# async def delete_campaign(campaign_id: UUID):
#     query = (
#         discount_campaigns.delete()
#         .where(discount_campaigns.c.campaign_id == campaign_id)
#         .returning(discount_campaigns.c.campaign_id)
#     )
#     result = await database.fetch_one(query)
#     if not result:
#         raise HTTPException(status_code=404, detail="Campaign not found")
#     return {"message": "Campaign deleted successfully"}