import datetime
from google.cloud import storage
from fastapi import UploadFile

class GCSService:
    def __init__(self):
        self.client = storage.Client()

    async def upload_file(self, file: UploadFile, bucket_name: str, destination_blob_name: str):
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload using stream to handle multiple file types efficiently
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)
        
        return blob

    def generate_signed_url(self, bucket_name: str, blob_name: str, expiration_minutes: int = 60):
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_minutes),
            method="GET",
        )
        
        # Calculate readable expiration time
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiration_minutes)
        
        return url, expiration_time

gcs_service = GCSService()