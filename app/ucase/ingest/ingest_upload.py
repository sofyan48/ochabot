import os
from fastapi import Form, File, UploadFile, Depends, HTTPException, status
from app.appctx import IResponseBase, response
from pkg.loader import loader as loader_model
from fastapi.security import HTTPAuthorizationCredentials
from pkg import utils
from datetime import datetime
from app.entity.ingest_document import IngestDocument
from app.ucase.ingest import (
    router, 
    auth, 
    logger, 
    splitter,
    UPLOAD_MODEL_DIR,
    minio_client,
    ingest_docs_repo
)

@router.post("/ingest", tags=["ingest"], operation_id="ingest_preview")
async def ingest_preview(
    chunk: int = Form(...),
    overlap: int = Form(...),
    file: UploadFile = File(...),
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IResponseBase:
    

    auth_payload = authorization.get('payload')
    if auth_payload.get('roles') != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please use user mode if you ingest data"
        )

    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)

    file_extension = os.path.splitext(file.filename)[1] 
    file_name = utils.generate_random_string(16)+file_extension
    file_path = os.path.join(UPLOAD_MODEL_DIR, file_name)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    data = None
    if (file_extension == ".pdf"):
        data = loader_model.pdf_loader(file_path)
    elif (file_extension == ".csv"):
        data = loader_model.csv_loader(file_path)
    elif (file_extension== ".text"):
        data = loader_model.text_loader(file_path)
    else:
        return response(
            message="Please select loader: text, pdf, csv",
            data=None
        )
    try:
        result = splitter.text_splitter(data=data, chunk=chunk, overlap=overlap)
    except Exception as e:
        logger.error("Error preview text splitter", {
            "error", e
        })

    ingest_code = utils.generate_random_string(6)
    client = auth_payload.get("username")
    
    bucket_path = "ingest/"+client+"/"+ingest_code+"/"+file_name

    try:
        minio_client.save(bucket_path, file_path=file_path)
    except Exception as e:
        logger.error("Error Uploading files",
            {
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="File not upload please try again"
        )

    entity_ingest_docs = IngestDocument(
        ingest_code=ingest_code,
        file_path=bucket_path,
        overlap=overlap,
        chunk=chunk,
        is_build= False,
        created_at=datetime.now(),
        updated_at= datetime.now(),
    )

    try:
        last_id = await ingest_docs_repo.upsert(entity_ingest_docs)
        entity_ingest_docs.id = last_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ingestion docs save to db error"
        )
    
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error("Error removing file", {
            "error": str(e)
        })

    return response(
        message="Preview text splitter",
        data={
            "ingest": entity_ingest_docs.to_dict(),
            "result": result
        }
    )
