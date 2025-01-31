from minio import Minio
from datetime import timedelta

class StorageMinio:
    _instance = None
    _minio = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StorageMinio, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def configure(cls, url: str, access_key: str, secret_key: str, is_secure: bool = False ):
        if cls._instance is None:
            cls._instance = super(StorageMinio, cls).__new__(cls)
        
        if cls._minio is None:
            cls._minio = Minio(
                endpoint=url,
                access_key=access_key,
                secret_key=secret_key,
                secure=is_secure
            )
        return cls._minio
    
    @classmethod
    def save(cls, bucket: str, object_name: str, file_path: str, content_type="application/octet-stream"):
        try:
            return cls._minio.fput_object(
                bucket_name=bucket,
                object_name=object_name,
                file_path=file_path,
                content_type=content_type
            )
        except Exception as e:
            raise e
        
    @classmethod
    def read(cls,  bucket: str, object_name: str, file_path: str):
        try:
            return cls._minio.fget_object(
                bucket_name=bucket,
                object_name=object_name,
                file_path=file_path
            )
        except Exception as e:
            raise e
        
    @classmethod
    def get_presign_url(cls, bucket: str, object_name: str, method: str, expiry: timedelta = timedelta(hours=1)):
        try:
            return cls._minio.get_presigned_url(
                method=method,
                bucket_name=bucket,
                object_name=object_name,
                expires=expiry
            )
        except Exception as e:
            raise e
    
    @classmethod
    def remove(cls,  bucket: str, object_name: str):
        try:
            return cls._minio.remove_object(
                bucket_name=bucket,
                object_name=object_name
            )
        except Exception as e:
            raise e