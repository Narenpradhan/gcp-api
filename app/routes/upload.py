from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.gcs_service import gcs_service
from typing import Optional

router = APIRouter()

@router.post("/upload")
async def upload_to_gcs(
    file: UploadFile = File(...),
    bucket_path: str = Form(...), # e.g., "folder/subfolder/filename.jpg"
    bucket_name: Optional[str] = Form(None),
    expiration_minutes: int = Form(60)
):
    try:
        # Use provided bucket or fallback to config
        from app.config import settings
        target_bucket = bucket_name or settings.default_bucket_name
        
        # 1. Upload the file
        blob = await gcs_service.upload_file(file, target_bucket, bucket_path)
        
        # 2. Generate Signed URL
        signed_url, expiry = gcs_service.generate_signed_url(
            target_bucket, bucket_path, expiration_minutes
        )

        return {
            "message": "File uploaded successfully",
            "file_path": f"gs://{target_bucket}/{bucket_path}",
            "signed_url": signed_url,
            "expires_at": expiry.isoformat(),
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))