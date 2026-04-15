import os
import uuid
import json
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
DATA_FILE = BASE_DIR / "products.json"

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/frontend", StaticFiles(directory=str(BASE_DIR.parent / "frontend")), name="frontend")


def load_products() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_products(products: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")


@app.get("/")
async def root():
    return FileResponse(str(BASE_DIR.parent / "frontend" / "index.html"))


@app.get("/api/products")
async def get_products():
    return load_products()


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Produit introuvable")


@app.post("/api/products")
async def create_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    photos: list[UploadFile] = File(...),
):
    product_id = str(uuid.uuid4())
    product_dir = UPLOAD_DIR / product_id
    product_dir.mkdir(exist_ok=True)

    photo_paths: list[str] = []
    for photo in photos:
        ext = Path(photo.filename or "img.jpg").suffix or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = product_dir / filename
        content = await photo.read()
        file_path.write_bytes(content)
        photo_paths.append(f"/uploads/{product_id}/{filename}")

    product = {
        "id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "photos": photo_paths,
    }

    products = load_products()
    products.append(product)
    save_products(products)

    return product


@app.put("/api/products/{product_id}")
async def update_product(
    product_id: str,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    photos: list[UploadFile] = File(None),
):
    products = load_products()
    product = None
    for p in products:
        if p["id"] == product_id:
            product = p
            break
    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    product["name"] = name
    product["description"] = description
    product["price"] = price

    if photos and photos[0].filename:
        product_dir = UPLOAD_DIR / product_id
        product_dir.mkdir(exist_ok=True)
        photo_paths: list[str] = []
        for photo in photos:
            ext = Path(photo.filename or "img.jpg").suffix or ".jpg"
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = product_dir / filename
            content = await photo.read()
            file_path.write_bytes(content)
            photo_paths.append(f"/uploads/{product_id}/{filename}")
        product["photos"] = photo_paths

    save_products(products)
    return product


@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str):
    products = load_products()
    new_products = [p for p in products if p["id"] != product_id]
    if len(new_products) == len(products):
        raise HTTPException(status_code=404, detail="Produit introuvable")

    import shutil
    product_dir = UPLOAD_DIR / product_id
    if product_dir.exists():
        shutil.rmtree(product_dir)

    save_products(new_products)
    return {"message": "Produit supprimé"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)