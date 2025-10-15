from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from bson import ObjectId
from database import db
from models import Product
import shutil
import os

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🟢 Create Product
@router.post("/")
async def create_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None)
):
    image_url = None
    if image:
        # create a safe filename
        filename = image.filename.replace(' ', '_')
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        # store path relative so frontend can fetch via /uploads/
        image_url = os.path.join(UPLOAD_DIR, filename).replace('\\', '/')

    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "image_url": image_url
    }

    result = await db.products.insert_one(product_data)
    return {"_id": str(result.inserted_id), **product_data}


# 🟢 Get All Products
@router.get("/")
async def get_products():
    products = []
    async for product in db.products.find():
        product["_id"] = str(product["_id"])
        products.append(product)
    return products


# 🟢 Get Product by ID
@router.get("/{product_id}")
async def get_product(product_id: str):
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])
    return product


# 🟡 Update Product
@router.put("/{product_id}")
async def update_product(product_id: str, product: Product):
    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or no change")
    updated = await db.products.find_one({"_id": ObjectId(product_id)})
    updated["_id"] = str(updated["_id"])
    return updated


# 🔴 Delete Product
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
