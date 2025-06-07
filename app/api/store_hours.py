from fastapi import APIRouter, HTTPException
from app.db import database
from uuid import UUID
from app.models.store_hours import store_operating_hours as store_table
from app.schemas.store_hours import StoreHourCreate,StoreHourUpdate,StoreHourOut


router = APIRouter(prefix="/admin/store-hours", tags=["Store Hours"])

# Create
# @router.post("/",response_model=StoreHourOut)
# async def create_store_hours(entry:StoreHourCreate):
#     query = store_table.insert().values(**entry.dict())
#     hour_id = await database.execute(query)
#     return {**entry.dict(), "id": hour_id, "created_at": None, "updated_at": None}

@router.post("/", response_model=StoreHourOut)
async def create_store_hours(payload: StoreHourCreate):
    query = store_table.insert().values(**payload.dict())
    inserted_id = await database.execute(query)

    # ✅ Fetch the full inserted record
    fetch_query = store_table.select().where(store_table.c.id == inserted_id)
    row = await database.fetch_one(fetch_query)
    return row  # FastAPI + Pydantic will serialize this correctly


# Get
@router.get("/", response_model=list[StoreHourOut])
async def get_all_store_hours():
    query = store_table.select()
    return await database.fetch_all(query)

@router.put("/{hour_id}", response_model=dict)
async def update_store_hour(hour_id: UUID, update: StoreHourUpdate):
    query = store_table.update().where(store_table.c.id == hour_id).values(**update.dict(exclude_unset=True))
    await database.execute(query)
    return {"message": "Store operating hours updated"}

@router.delete("/{hour_id}", response_model=dict)
async def delete_store_hour(hour_id: UUID):
    query = store_table.delete().where(store_table.c.id == hour_id)
    await database.execute(query)
    return {"message": "Store operating hours deleted"}