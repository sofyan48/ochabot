from fastapi import Header, HTTPException

async def session_middleware(x_session: str = Header(None)):
    if x_session is None:
       raise HTTPException(status_code=400, detail="Missing x-session header")
    return x_session