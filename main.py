from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import product_routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Product Catalog System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include API router
app.include_router(product_routes.router)

# make sure static folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("frontend", exist_ok=True)

# serve frontend files under /static and uploaded images under /uploads
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    # serve the home page
    return FileResponse("frontend/home.html")
