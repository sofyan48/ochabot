from app.library import minio
from pkg.storage.minio import StorageMinio
import os

class Storage(object):
    def __init__(self, minio: StorageMinio):
        self.minio = minio
        self.bucket = os.environ.get("STORAGE_BUCKET")

    def save(self, name: str, file_path: str):
        try:
            return self.minio.save(
                bucket=self.bucket,
                object_name=name,
                file_path=file_path
            )
        except Exception as e:
            raise e
    
    def read(self, name: str, file_path: str):
        try:
            return self.minio.read(
                bucket=self.bucket,
                object_name=name,
                file_path=file_path
            )
        except Exception as e:
            print("PROBLEM", e)
            raise e
        
    def get_presign_url(self, name: str):
        try:
            return self.minio.get_presign_url(
                method="GET",
                bucket=self.bucket,
                object_name=name
            )
        except Exception as e:
            raise e
        
    def remove(self, name:str):
        try:
            return self.minio.remove(
                bucket=self.bucket,
                object_name=name
            )
        except Exception as e:
            raise e