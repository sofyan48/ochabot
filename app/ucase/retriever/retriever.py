import os
from fastapi import Form, File, UploadFile, Depends
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth
from app.ucase.retriever import router, auth, logger, chromadb, UPLOAD_MODEL_DIR

@router.post("/retriever/chroma")
async def build_retriever_chroma(collection: str = Form(...),
    loader: str = Form(...),
    chunk: int = Form(...),
    overlap: int = Form(...),
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    
    auth.authenticate(credentials=credentials)
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)
    
    file_path = os.path.join(UPLOAD_MODEL_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    data = None
    if (loader == "pdf"):
        data = loader_model.pdf_loader(file_path)
    elif (loader == "csv"):
        data = loader_model.csv_loader(file_path)
    elif (loader== "text"):
        data = loader_model.text_loader(file_path)
    else:
        return response(
            message="Please select loader: text, pdf, csv",
            data=None
        )
    chromadb.build(data=data, collection=collection, chunk=chunk, overlap=overlap)
    logger.info("Chroma Building", {
        "loader": loader,
        "path": file_path, 
        "chunk": chunk,
        "overlap": overlap
    })
    
    return response(
        message="Retriver build",
        data={
            "collection": collection,
            "file": file_path
        }
    )
