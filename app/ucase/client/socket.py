from app.ucase.client import client_socket_repo, router, auth, logger
from app.ucase.client import router
from app.presentation import request
from fastapi.security import HTTPBasicCredentials
from fastapi import Depends, Query, HTTPException, status
from app.appctx import IGetResponseBase, response
from app.ucase import BasicAuth
from datetime import datetime
from pkg import utils
from typing import Optional

@router.post("/client/socket", tags=["client"], operation_id="insert_client_socket") 
async def insert_client_socket(payload: request.RequestClientSocket,
                        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
                    ) -> IGetResponseBase:
    auth.authenticate(credentials)

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
        return HTTPException(status_code=500, detail="Cannot upsert client socket")
    return response(
        message="Successfully",
        data=client
    )

@router.get("/client/socket", tags=["client"])
async def list_client_socket(
        limit: Optional[int] = Query(None, description="Limit"),
        page: Optional[int] = Query(None, description="page"),
        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
    ) -> IGetResponseBase:
    auth.authenticate(credentials)

    try:
        list_data = await client_socket_repo.list(limit=limit, page=page)
    except Exception as e:
        return HTTPException(
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
        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
    ) -> IGetResponseBase:
    auth.authenticate(credentials)

    try:
        data = await client_socket_repo.fetch(id=id)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e
            }
        )

    return response(
        message="Getting client socket successfully",
        data=data
    )

@router.delete("/client/socket/{id}", tags=["client"])
async def detail_client_socket(id: int,
        credentials: HTTPBasicCredentials = Depends(BasicAuth().security),
    ) -> IGetResponseBase:
    auth.authenticate(credentials)

    try:
        await client_socket_repo.delete(id=id)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e
            }
        )

    return response(
        message="Delete client socket successfully",
        data={}
    )
