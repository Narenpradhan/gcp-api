from fastapi import FastAPI
from app.routes import upload

app = FastAPI(title="GCS File Manager API")

# Include routes
app.include_router(upload.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)