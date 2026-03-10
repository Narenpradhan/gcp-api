from fastapi import FastAPI
from app.routes import upload

app = FastAPI(
    title="GCS Signed URL API",
    description="API to upload files and get temporary access URLs using raw SMK credentials"
)

# Include our upload routes
app.include_router(upload.router, prefix="/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Use uv run uvicorn ... or just python -m uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)