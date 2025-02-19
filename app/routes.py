import validators
from fastapi import APIRouter, HTTPException, Request, Depends, Security
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse, Response
from app.services import generate_id, validate_url, verify_token
from app.models import SessionDep, select, URLModel, delete
from app.schemas import URLSchema

router = APIRouter()
sec = HTTPBearer()

@router.get("/", status_code=200)
def list_keys(session: SessionDep):
    keys = session.exec(select(URLModel.value)).all()
    if not keys:
        return JSONResponse({}, status_code=200)
    return JSONResponse(keys, status_code=200)

@router.post("/", status_code = 201)
def shorten_url(item: URLSchema, session: SessionDep, token: str = Security(sec)):

    user = verify_token(token.credentials)

    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not validators.url(item.value):
        raise HTTPException(status_code=400, detail="error: Invalid URL")
    

    entry = session.exec(select(URLModel).where(URLModel.url == item.value, URLModel.username == user["sub"])).first()
    if entry:
        session.delete(entry)
        session.commit()
    
    shorten_url = URLModel(url=item.value, value=generate_id(item.value), username=user["sub"])
    session.add(shorten_url)
    session.commit()

    # entry = session.exec(select(URLModel).where(URLModel.url == item.value)).first()
    # if entry:
    #     session.delete(entry)
    #     session.commit()       

    # shorten_url = URLModel(url=item.value, value=generate_id(item.value))
    # session.add(shorten_url)
    # session.commit()

    return {"id": shorten_url.value}

@router.delete("/" , status_code=404) 
def delete_nothing(session: SessionDep, token: str = Security(sec)):
    user = verify_token(token.credentials)

    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")

    session.exec(delete(URLModel))
    session.commit()
    return JSONResponse(status_code=404, content={})

@router.get("/{url_key}", status_code=301)
def redirect_url(url_key: str, session: SessionDep, token: str = Security(sec)):
    user = verify_token(token.credentials)

    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")

    entry = session.exec(select(URLModel).where(URLModel.value == url_key)).first()#, URLModel.username == user["sub"])).first()

    if not entry:
        raise HTTPException(status_code=404, detail="error: URL not found")    

    return {"value": entry.url}

@router.put("/{url_key}", status_code=200)
async def update_url(url_key: str, url: URLSchema, session: SessionDep, token: str = Security(sec)):
    user = verify_token(token.credentials)

    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")

    # entry = session.exec(select(URLModel).where(URLModel.value == url_key, URLModel.username == user["sub"])).first()
    entry = session.exec(select(URLModel).where(URLModel.value == url_key)).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="error: URL not found")

    if not url.value or not validate_url(url.value): 
        raise HTTPException(status_code=400, detail="error: Invalid URL")
    
    shorten_url = URLModel(url=url.value, value=url_key, username=user["sub"])

    session.delete(entry)
    session.commit()   

    session.add(shorten_url)
    session.commit()

    return {"value": shorten_url.value}

@router.delete("/{url_key}", status_code=204)
def delete_url(url_key: str, session: SessionDep, token: str = Security(sec)):

    user = verify_token(token.credentials)
    if not user:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # url = session.exec(select(URLModel).where(URLModel.value == url_key, URLModel.username == user["sub"])).first()
    url = session.exec(select(URLModel).where(URLModel.value == url_key)).first()

    if not url:
        raise HTTPException(status_code=404, detail="error: URL not found")

    session.delete(url)
    session.commit()
    
    return Response(status_code=204)
