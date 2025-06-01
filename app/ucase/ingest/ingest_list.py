import os
from fastapi import Query, Depends, HTTPException, status
from app.appctx import IResponseBase, response
from pkg import utils
from fastapi.security import HTTPAuthorizationCredentials
from typing import Optional
from app.ucase.ingest import (
    router, 
    auth, 
    logger, 
    UPLOAD_MODEL_DIR,
    minio_client,
    ingest_docs_repo
)

@router.get("/ingest", tags=["ingest"], operation_id="ingest_document_list")
async def ingest_document_list(
    limit: Optional[int] = Query(10, description="Limit"),
    page: Optional[int] = Query(1, description="page"),
    authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)) -> IResponseBase:
    
    if not os.path.exists(UPLOAD_MODEL_DIR):
        os.makedirs(UPLOAD_MODEL_DIR)

    try:
        document_list = await ingest_docs_repo.fetch(limit=limit, page=page)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ingest not found"
        )
    result = []
    for i in document_list:
        url = minio_client.get_presign_url(i.get('file_path'))
        result.append(
            {
                'id': i.get('id'), 
                'ingest_code': i.get('ingest_code'), 
                'file_path': url, 
                'overlap': i.get('overlap'), 
                'chunk': i.get('chunk'),
                'collection': i.get('collection'),
                'is_build': i.get('is_build'), 
                'created_at': i.get('created_at'), 
                'updated_at': i.get('updated_at')
            }
        )
    return response(
        message="Preview text splitter",
        data=utils.json_serializable(result)
    )
