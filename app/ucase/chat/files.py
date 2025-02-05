import os
from fastapi import Form, File, UploadFile, Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase import session_middleware
from app.ucase.chat import (
    router, 
    auth, 
    logger,
    UPLOAD_MODEL_DIR,
    minio_client
)

@router.post("/chat/files", tags=["chat"], operation_id="upload_files")
async def chat_with_files(
    file: UploadFile = File(...),
    x_session: str = Depends(session_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    
    session_path = os.path.normpath(os.path.join(UPLOAD_MODEL_DIR, x_session))
    if not session_path.startswith(UPLOAD_MODEL_DIR):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid session path"
        )
    if not os.path.exists(session_path):
        os.makedirs(session_path)

    file_path = os.path.normpath(os.path.join(session_path, file.filename))
    if not file_path.startswith(session_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file path"
        )
    with open(file_path, "wb") as f:
        f.write(await file.read())

    bucket_path = "chat/"+x_session+"/"+file.filename

    try:
        minio_client.save(bucket_path, file_path=file_path)
        url_file = minio_client.get_presign_url(bucket_path)
        os.remove(file_path)
    except Exception as e:
        logger.error(
            "Error Uploading files",
            {
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="File not upload please try again"
        )
    
    return response(
        message="Successfully",
        data={
            "url": url_file,
        },
    )
