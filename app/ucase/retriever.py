from fastapi import APIRouter, Form, File, UploadFile, Depends
from app.appctx import IGetResponseBase, response
from app import retriever_chroma, UPLOAD_MODEL_DIR
from pkg.retriever import loader
from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth
import os, random

router = APIRouter()

@router.post("/retriever/chroma")
async def build_retriever_chroma(collection: str = Form(...),
    load: str = Form(...),
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)
) -> IGetResponseBase:
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)
    
    file_path = os.path.join(UPLOAD_MODEL_DIR, random.choice(word_list) for _ in range(count)+file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    data = None
    if (load == "pdf"):
        data = loader.pdf_loader(file_path)
    elif (load == "csv"):
        data = loader.csv_loader(file_path)
    elif (load== "json"):
        data = loader.json_loader(file_path)
    else:
        return response(
            message="Please select loader: json, pdf, csv",
            data=None
        )
    retriever_chroma.build(data=data, collection=collection)
    return response(
        message="Retriver build",
        data={
            "collection": collection,
            "file": file_path
        }
    )