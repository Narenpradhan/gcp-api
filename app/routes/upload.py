from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.gcs_service import gcs_service
from app.config import settings
from typing import Optional

router = APIRouter()

@router.post("/upload")
async def upload_and_sign(
    file: UploadFile = File(...),
    bucket_path: str = Form(...),  # e.g. "profiles/user_1/avatar.png"
    bucket_name: Optional[str] = Form(None),
    expiration_minutes: int = Form(60)
):
    try:
        # 1. Determine target bucket
        target_bucket = bucket_name or settings.default_bucket_name
        
        # 2. Upload to GCS
        await gcs_service.upload_file(file, target_bucket, bucket_path)
        
        # 3. Generate the Signed URL
        signed_url, expires_at = gcs_service.generate_signed_url(
            target_bucket, 
            bucket_path, 
            expiration_minutes
        )

        return {
            "status": "success",
            "upload_details": {
                "bucket": target_bucket,
                "file_path": bucket_path,
                "content_type": file.content_type
            },
            "access_details": {
                "signed_url": signed_url,
                "expires_at_utc": expires_at.isoformat(),
                "valid_for_minutes": expiration_minutes
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCS Error: {str(e)}")