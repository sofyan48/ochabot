from pkg.storage.minio import StorageMinio
import os

def register_storage_minio():
    return StorageMinio.configure(
        url=os.environ.get("MINIO_URL", "localhost:9000"),
        access_key=os.environ.get("MINIO_ACCESSKEY", "ACCESS_KEY"),
        secret_key=os.environ.get("MINIO_SECRETKEY", "SECRET_KEY")
    )