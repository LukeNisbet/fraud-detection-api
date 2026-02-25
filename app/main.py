import os
from fastapi import FastAPI
from app.api import router

# Check if we are on your laptop or the live internet
ENV = os.getenv("ENV", "development")

# Security switch: Hide Swagger UI if we are in production
if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(title="Fraud Detection API [DEV]")

# Plug include the mapping of URLs to python functions defined in the api.py file
app.include_router(router)

@app.get("/") #this maps the "/" URL to the health check function
def health_check():
    # We add the environment here so you can verify your security settings
    return {
        "status": "healthy", 
        "message": "Fraud API is running!",
        "mode": ENV
    }