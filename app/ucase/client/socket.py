from app.ucase.client import client_socket_repo, router, auth, logger
from app.ucase.client import router
from app.presentation import request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, Query, HTTPException, status
from app.appctx import IGetResponseBase, response
from datetime import datetime
from pkg import utils
from typing import Optional

@router.post("/client/socket", tags=["client"], operation_id="insert_client_socket") 
async def insert_client_socket(
        payload: request.RequestClientSocket,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IGetResponseBase:
    client = {
        "name": payload.name,
        "secret": utils.generate_random_string(16),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    if payload.id is not None:
        client['id'] = payload.id

    try:
        lastId = await client_socket_repo.upsert(client)
        client['id'] = lastId
    except Exception as e:
        logger.error("Cannot upsert client socker", {
            "error": e
        })
        raise HTTPException(status_code=500, detail="Cannot upsert client socket")
    return response(
        message="Successfully",
        data=client
    )

@router.get("/client/socket", tags=["client"])
async def list_client_socket(
        limit: Optional[int] = Query(None, description="Limit"),
        page: Optional[int] = Query(None, description="page"),
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IGetResponseBase:

    try:
        list_data = await client_socket_repo.list(limit=limit, page=page)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e
            }
        )

    return response(
        message="List data",
        data=list_data
    )

@router.get("/client/socket/{id}", tags=["client"])
async def detail_client_socket(id: int,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate)
    ) -> IGetResponseBase:

    try:
        data = await client_socket_repo.fetch(id=id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal failure"
        )

    return response(
        message="Getting client socket successfully",
        data=data
    )

@router.delete("/client/socket/{id}", tags=["client"])
async def detail_client_socket(id: int,
        authorization: HTTPAuthorizationCredentials = Depends(auth.authenticate),
    ) -> IGetResponseBase:

    try:
        await client_socket_repo.delete(id=id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Failure"
        )

    return response(
        message="Delete client socket successfully",
        data={}
    )
