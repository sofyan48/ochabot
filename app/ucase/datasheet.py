from fastapi import APIRouter, HTTPException, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import APP_ROOT
from pkg import utils
import csv
from fastapi.security import HTTPBasicCredentials
from app.ucase import session_middleware, BasicAuth


router = APIRouter()
@router.post("/datasheet")
async def add_datasheet(payload: request.RequestDatasheet, credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    csvPath = APP_ROOT+"/knowledge/data.csv"
    try:
        csvLastData = await utils.read_last_row_from_csv(csvPath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    lastIDS = ""
    for i in csvLastData:
        lastIDS = i[0]

    try:
        csvData = await utils.read_csv(csvPath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    ids = int(lastIDS)+1
    question = str(payload.question).replace(",", " ")
    answer = str(payload.answer).replace(",", " ")
    csvData.append([str(ids), question, '"'+answer+'"'])
    
    with open(csvPath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csvData)
    
    return response(
        message="Datasheet inserted",
        data={
            "ids": ids,
            "question": question,
            "answer": answer
        },
        meta={}
    )
