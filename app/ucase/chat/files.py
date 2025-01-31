import os
from fastapi import Form, File, UploadFile, Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth, session_middleware
from pkg.history import MessageHistory
from pkg import utils
from app.ucase.chat import (
    router, 
    auth, 
    logger, 
    chromadb, 
    llm_platform,
    setup_repo,
    alchemy,
    UPLOAD_MODEL_DIR,
    minio_client
)

@router.post("/chat/files", tags=["chat"], operation_id="upload_files")
async def chat_with_files(
    file: UploadFile = File(...),
    x_session: str = Depends(session_middleware),
    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    
    auth.authenticate(credentials=credentials)
    if not os.path.exists(UPLOAD_MODEL_DIR+"/"+x_session):
        os.makedirs(UPLOAD_MODEL_DIR+"/"+x_session)

    file_path = os.path.join(UPLOAD_MODEL_DIR, file.filename)
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
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="File not upload please try again"
        )
    
    return response(
        message="Successfully",
        data={
            "url": url_file,
        },
    )
