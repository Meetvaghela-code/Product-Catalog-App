Product Catalog App

This is a simple FastAPI + MongoDB project that demonstrates a product catalog with image uploads and a lightweight frontend.

Pages:
- / -> Home (served from `frontend/home.html`)
- /static/add_product.html -> Form to add products
- /static/dashboard.html -> Dashboard that lists products
- /static/product_manager.html -> Original single-page manager

Run (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start MongoDB (ensure mongod is running)
uvicorn main:app --reload --port 8000
```

Uploads are stored in `uploads/` and served at `/uploads/<filename>`.

APIs:
- GET /products
- GET /products/{id}
- POST /products (multipart/form-data)
- PUT /products/{id} (JSON body matching Product model)
- DELETE /products/{id}

Notes:
- Adjust MongoDB connection in `database.py` if needed.
- This is a minimal demo; consider adding authentication and validation for production.
