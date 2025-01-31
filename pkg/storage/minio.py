from minio import Minio

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
        return cls._minio.fput_object(
            bucket_name=bucket,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )