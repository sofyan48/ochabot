import os
from fastapi import Depends, HTTPException, status
from app.presentation import request
from app.appctx import IResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPAuthorizationCredentials
from pkg import utils
from datetime import datetime
from app.ucase.ingest import (
    router, 
    auth, 
    logger, 
    chromadb, 
    UPLOAD_MODEL_DIR,
    minio_client,
    ingest_docs_repo,
    setup_repo,
    vectorstoreDB
)

@router.post("/ingest/vector", tags=["ingest"], operation_id="build_ingest_vector")
async def build_ingest_vector(
    payload: request.RequestIngestVector,
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IResponseBase:
    
    setup = await setup_repo.get_all_setup()
    auth_payload = authorization.get('payload')
    if auth_payload.get('roles') != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please use user mode if you ingest data"
        )
    
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)
    
    try:
        ingest_docs_data = await ingest_docs_repo.fetch_row_by_ingest_code(payload.ingest_code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Getting ingest code error"
        )
    
    if ingest_docs_data.is_build is True:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Document have build"
        )
    
    file_path = "./storage/"+ingest_docs_data.file_path
    try:
        minio_client.read(name=ingest_docs_data.file_path, file_path=file_path)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot get file from storage"
        )
    file_extension = os.path.splitext(file_path)[1]
    
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
        vector_db_config = setup.get('config:retriever:vector_db')
    except Exception:
        logger.info("Using default setup for chroma")
        vector_db_config = "chroma"

    try:
        
        vector_db= vectorstoreDB.configure(vectorestore=vector_db_config)
        vector_db.build(data=data, collection=payload.collection, chunk=ingest_docs_data.chunk, overlap=ingest_docs_data.overlap)
    except Exception as e:
        logger.error("Error building data", {
            "error", e
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot build ingest data"
        )
    
    entity_ingest_docs = {
        "id": ingest_docs_data.id,
        "ingest_code": ingest_docs_data.ingest_code,
        "file_path": ingest_docs_data.file_path,
        "overlap": ingest_docs_data.overlap,
        "collection": payload.collection,
        "is_build": True,
        "chunk": ingest_docs_data.chunk,
        "updated_at": datetime.now()
    }

    try:
        await ingest_docs_repo.upsert(entity_ingest_docs)
    except Exception as e:
        logger.error("Error update ingest status", {
            "error", e
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error update ingest status"
        )

    os.remove(file_path)
    return response(
        message="Ingestion Success on: "+ vector_db_config,
        data=utils.json_serializable(ingest_docs_data)
    )
