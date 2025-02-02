import os
from fastapi import Form, File, UploadFile, Depends
from typing import Optional
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPAuthorizationCredentials
from app.ucase.retriever import (
    router, 
    auth, 
    logger, 
    chromadb, 
    UPLOAD_MODEL_DIR
)

@router.post("/retriever/chroma", tags=["retriever"], operation_id="build_retriever_chroma")
async def build_retriever_chroma(collection: str = Form(...),
    chunk: int = Form(...),
    overlap: int = Form(...),
    file: UploadFile = File(...),
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IGetResponseBase:
    
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)
    
    file_path = os.path.join(UPLOAD_MODEL_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_extension = os.path.splitext(file.filename)[1] 
    data = None
    logger.info("Splitting Process")
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
    logger.info("Splitting Success")
    try:
        chromadb.build(data=data, collection=collection, chunk=chunk, overlap=overlap)
    except Exception as e:
        logger.error("Error building chroma", {
            "error", e
        })

    logger.info("Chroma Building", {
        "path": file_path, 
        "chunk": chunk,
        "overlap": overlap
    })
    return response(
        message="Retriver build",
        data={
            "collection": collection,
            "file": file_path,
        }
    )
