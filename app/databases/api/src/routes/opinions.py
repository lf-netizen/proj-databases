import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from clients.mongodb import mongodb
from models.opinion import Opinion, OpinionUpdate

ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])
collection = mongodb[ROUTE_NAME]


@router.get("/", response_model=List[Opinion])
async def get_all_opinions(
    user_id: Optional[int] = Query(None),
    product_id: Optional[str] = Query(None)
):
    query = {}
    if user_id is not None:
        query["user_id"] = user_id
    if product_id is not None:
        query["product_id"] = product_id

    opinions = list(collection.find(query))
    return opinions


@router.post("/", response_model=Opinion)
async def create_opinion(opinion: Opinion):
    opinion_data = opinion.dict()
    inserted_opinion = collection.insert_one(opinion_data)
    return {"id": str(inserted_opinion.inserted_id), **opinion_data}


@router.get("/{opinion_id}", response_model=Opinion)
async def read_opinion(opinion_id: str):
    opinion = collection.find_one({"id": opinion_id})
    if opinion:
        return opinion
    else:
        raise HTTPException(status_code=404, detail="Opinion not found")


@router.put("/{opinion_id}", response_model=Opinion)
async def update_opinion(opinion_id: str, opinion: Opinion):
    opinion_data = opinion.dict() | {"id": opinion_id}
    updated_opinion = collection.update_one(
        {"id": opinion_id}, {"$set": opinion_data})
    if updated_opinion.modified_count == 1:
        return {"message": "Opinion updated successfully", **opinion_data}
    else:
        raise HTTPException(status_code=404, detail="Opinion not found")


@router.patch("/{opinion_id}", response_model=OpinionUpdate)
async def patch_opinion(opinion_id: str, opinion_update: OpinionUpdate):
    opinion_data = opinion_update.dict(exclude_unset=True)
    if not opinion_data:
        raise HTTPException(
            status_code=400, detail="No fields provided for update")
    updated_opinion = collection.update_one(
        {"id": opinion_id}, {"$set": opinion_data})
    if updated_opinion.modified_count == 1:
        return {"message": "Opinion patched successfully", **opinion_data}
    else:
        raise HTTPException(status_code=404, detail="Opinion not found")


@router.delete("/{opinion_id}", response_model=dict)
async def delete_opinion(opinion_id: str):
    deleted_opinion = collection.delete_one({"id": opinion_id})
    if deleted_opinion.deleted_count == 1:
        return {"message": "Opinion deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Opinion not found")

