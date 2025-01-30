import os
from fastapi import Form, File, UploadFile, Depends, HTTPException, status
from app.appctx import IGetResponseBase, response
from pkg.retriever import loader as loader_model
from fastapi.security import HTTPBasicCredentials
from app.ucase import BasicAuth, session_middleware
from pkg.history import MessageHistory
from pkg import utils
from app.ucase.chat import (
    router, 
    auth, 
    logger, 
    chromadb, 
    llm_platform,
    setup_repo,
    alchemy,
    UPLOAD_MODEL_DIR
)

@router.post("/chat/files", tags=["chat"], operation_id="chat_with_files")
async def chat_with_files(
    chat: str = Form(...),
    file: UploadFile = File(...),
    x_session: str = Depends(session_middleware),
    credentials: HTTPBasicCredentials = Depends(BasicAuth().security)) -> IGetResponseBase:
    
    auth.authenticate(credentials=credentials)
    if not os.path.exists(UPLOAD_MODEL_DIR+"/"+x_session):
        os.makedirs(UPLOAD_MODEL_DIR+"/"+x_session)


    file_path = os.path.join(UPLOAD_MODEL_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    file_extension = os.path.splitext(file.filename)[1]
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

    
    history = MessageHistory(alchemy, x_session).sql()
    history_msg = await history.aget_messages()
    setup = await setup_repo.get_all_setup()
    # validate model name
    try:
        platform = setup.get('config:llm:platform')
    except Exception:
        platform = "mistral"
    
    try:
        model = setup.get('config:llm:model')
    except Exception:
        model = None
       
    llm = llm_platform.initiate(platform, model=model)
    try: 
        top_k = int(setup.get('config:retriever:top_k'))
    except:
        top_k = 5

    try:
        fetch_k = int(setup.get('config:retriever:fetch_k'))
    except Exception:
        fetch_k = 10
    
    collection = x_session+"_"+utils.generate_random_string(10)
    chunk = 2000
    overlap = 500

    try:
        chromadb.build(data=data, collection=collection, chunk=chunk, overlap=overlap)
    except Exception as e:
        logger.error("Error building chroma", {
            "error", e
        })

    retriever = llm.retriever(
        top_k=top_k,
        fetch_k=fetch_k,
        collection=collection
    )
    
    qa_retrieval = llm.retrieval("", retriever=retriever)
    
    chain_with_history = llm.chain_with_history(
        qa_retrieval,
        history=history,
        input_messages_key="input",
        history_messages_key="message_store",
        output_messages_key="answer",
    )

    config = {"configurable": {"session_id": f'{x_session}'}}
    try:
        resultAI = await chain_with_history.ainvoke({"input": chat, "history": history_msg}, config=config)
    except Exception as e:
        logger.error("Invok message error", {
            "error": str(e)
        })
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Internal failure",
            )
    logger.info("AI Result", {
        "chat": chat,
        "file": file_path,
        "content": resultAI['answer'],
    })
    return response(
        message="Successfully",
        data={
            "result": resultAI['answer'],
        },
    )
