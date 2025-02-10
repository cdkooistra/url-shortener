import validators
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services import generate_id, validate_url
from app.models import SessionDep, select, URLModel, delete
from app.schemas import URLSchema

router = APIRouter()

@router.get("/", status_code=200)
def list_keys(session: SessionDep):
    keys = session.exec(select(URLModel.value)).all()
    if not keys:
        return JSONResponse({}, status_code=200)
    return JSONResponse(keys, status_code=200)

@router.post("/", status_code = 201)
def shorten_url(item: URLSchema, session: SessionDep):
    if not validators.url(item.value):
        raise HTTPException(status_code=400, detail="error: Invalid URL")
    
    entry = session.exec(select(URLModel).where(URLModel.url == item.value)).first()
    if entry:
        session.delete(entry)
        session.commit()       

    shorten_url = URLModel(url=item.value, value=generate_id(item.value))
    session.add(shorten_url)
    session.commit()

    return {"id": shorten_url.value}

@router.delete("/" , status_code=404) 
def delete_nothing(session: SessionDep):
    session.exec(delete(URLModel))
    session.commit()
    return JSONResponse(status_code=404, content={})

@router.get("/{url_key}", status_code=301)
def redirect_url(url_key: str, session: SessionDep):
    entry = session.exec(select(URLModel).where(URLModel.value == url_key)).first()

    if not entry:
        raise HTTPException(status_code=404, detail="error: URL not found")    

    return {"value": entry.url}

@router.put("/{url_key}", status_code=200)
async def update_url(url_key: str, request: Request, session: SessionDep):
    entry = session.exec(select(URLModel).where(URLModel.value == url_key)).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="error: URL not found")

    body = await request.json() # get the request body encoded in json
    new_url = body.get("url") # get the url from request body 

    if not new_url or not validate_url(new_url): 
        raise HTTPException(status_code=400, detail="error: Invalid URL")
    
    shorten_url = URLModel(url=entry.url, value=generate_id(new_url))

    session.delete(entry)
    session.commit()   

    session.add(shorten_url)
    session.commit()

    return {"value": shorten_url.value}

@router.delete("/{url_key}", status_code=204)
def delete_url(url_key: str, session: SessionDep):
    url = session.exec(select(URLModel).where(URLModel.value == url_key)).first()

    if not url:
        raise HTTPException(status_code=404, detail="error: URL not found")

    session.delete(url)
    session.commit()
    return JSONResponse(status_code=204, content={})
