import os
from fastapi import Depends, HTTPException, status
from app.presentation import request
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPAuthorizationCredentials
from pkg import utils
from app.ucase.ingest import (
    router, 
    auth, 
    logger, 
    chromadb, 
    UPLOAD_MODEL_DIR,
    minio_client,
    ingest_docs_repo
)

@router.post("/ingest/chroma", tags=["ingest"], operation_id="build_retriever_chroma")
async def build_retriever_chroma(
    payload: request.RequestIngestChroma,
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)
    
    try:
        ingest_docs_data = await ingest_docs_repo.fetch_row_by_ingest_code(payload.ingest_code)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Getting ingest code error"
        )
    
    file_path = "./storage/"+ingest_docs_data.file_path
    try:
        file = minio_client.read(name=ingest_docs_data.file_path, file_path=file_path)
    except Exception as e:
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
        chromadb.build(data=data, collection=payload.collection, chunk=ingest_docs_data.chunk, overlap=ingest_docs_data.overlap)
    except Exception as e:
        logger.error("Error building chroma", {
            "error", e
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot build chroma ingest"
        )
    os.remove(file_path)
    return response(
        message="Ingestion Success",
        data={
            "collection": payload.collection,
            "ingest_document": utils.json_serializable(ingest_docs_data)
        }
    )
