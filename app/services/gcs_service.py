import json
import datetime
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound # Added for validation
from fastapi import UploadFile, HTTPException
from app.config import settings

class GCSService:
    def __init__(self):
        try:
            key_info = json.loads(settings.gcp_raw_key)
            credentials = service_account.Credentials.from_service_account_info(key_info)
            self.client = storage.Client(
                credentials=credentials, 
                project=key_info.get("project_id")
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GCP Storage Client: {e}")

    def _check_bucket_exists(self, bucket_name: str):
        """Internal helper to verify bucket existence and permissions."""
        try:
            # This calls the GCP API to check if the bucket metadata is accessible
            self.client.get_bucket(bucket_name)
        except NotFound:
            raise HTTPException(status_code=404, detail=f"Bucket '{bucket_name}' not found.")
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"Access denied to bucket '{bucket_name}': {str(e)}")

    async def upload_file(self, file: UploadFile, bucket_name: str, destination_path: str):
        # 1. Validation Step
        self._check_bucket_exists(bucket_name)

        # 2. Upload Step
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_path)
        
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)
        
        return blob

    def generate_signed_url(self, bucket_name: str, blob_name: str, expiration_minutes: int):
        # Since we already validated the bucket in upload_file, 
        # we can proceed to sign directly.
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_minutes),
            method="GET",
        )
        
        expiry_timestamp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiration_minutes)
        return url, expiry_timestamp

gcs_service = GCSService()