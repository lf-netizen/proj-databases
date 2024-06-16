import os
from typing import List, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from clients.mongodb import mongodb
from clients.qdrant import QdrantManager
from models.product import Product, ProductUpdate
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct


ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])
collection = mongodb[ROUTE_NAME]
qdrant_manager = QdrantManager()


@router.get("/", response_model=List[Product])
async def get_all_products(
    category: List[str] | None = Query(None),
    tag: List[str] | None = Query(None)
):
    query = {}
    if category:
        query["category"] = {"$in": category}
    if tag:
        query["tags"] = {"$in": tag}

    return collection.find(query)


@router.post("/", response_model=Product)
async def create_product(product: Product):
    product_data = product.model_dump()
    inserted_product = collection.insert_one(product_data)
    await qdrant_manager.add_product_vec(product)
    return {"id": str(inserted_product.inserted_id), **product_data}


@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: str):
    product = collection.find_one({"id": product_id})
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# find product by name
@router.get("/name/{product_name}", response_model=Product)
async def read_product(product_name: str):
    product = collection.find_one({"name": product_name})
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    product_data = product.model_dump() | {"id": product_id}
    updated_product = collection.update_one(
        {"id": product_id}, {"$set": product_data})
    await qdrant_manager.update_product(product)
    if updated_product.modified_count == 1:
        return {"message": "Product updated successfully", **product_data}
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.patch("/{product_id}", response_model=ProductUpdate)
async def patch_product(product_id: str, product_update: ProductUpdate):
    product_data = product_update.model_dump(exclude_unset=True)
    if not product_data:
        raise HTTPException(
            status_code=400, detail="No fields provided for update")
    updated_product = collection.update_one(
        {"id": product_id}, {"$set": product_data})
    if updated_product.modified_count == 1:
        return {"message": "Product patched successfully", **product_data}
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    deleted_product = collection.delete_one({"id": product_id})
    if deleted_product.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

class QuestionRequest(BaseModel):
    question: str

@router.post("/vec_search/", response_model=List[Any])
async def vector_search(request: QuestionRequest):
    response = await qdrant_manager.search(request.question)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Vector DB error")