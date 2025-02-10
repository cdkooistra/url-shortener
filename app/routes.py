import validators
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services import generate_id, validate_url
from app.models import SessionDep, select, URLModel
from app.schemas import URLSchema

router = APIRouter()

def check_if_exists(url_key, session): 
    url = session.get(URLModel, url_key)

    if not url:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    return url

@router.get("/", status_code = 200)
def list_keys(session: SessionDep):
    return JSONResponse(session.exec(select(URLModel.value)).all(), status_code=200)

@router.post("/", status_code = 201)
def shorten_url(item: URLSchema, session: SessionDep):
    
    if not validators.url(item.value):
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    shorten_url = URLModel(value=generate_id(item.value))
    session.add(shorten_url)
    session.commit()

    return {"id": shorten_url}

@router.delete("/" , status_code = 404) 
def delete_nothing():
    raise HTTPException(status_code = 404, detail = "error: Not Supported (No ID)")

@router.get("/{url_key}", status_code=301)
def redirect_url(url_key: str, session: SessionDep):
    db_url = check_if_exists(url_key, session)

    return JSONResponse(status_code=301, content={"value": db_url.value})

@router.put("/{url_key}", status_code=200)
async def update_url(url_key: str, request: Request, session: SessionDep):
    old_url = check_if_exists(url_key, session)

    body = await request.json() # get the request body encoded in json
    new_url = body.get("url") # get the url from request body 

    if not new_url or not validate_url(new_url): 
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    shorten_url = URLModel(value=generate_id(new_url))
    session.delete(old_url)
    session.add(shorten_url)
    session.commit()
    return {"updated url key": shorten_url.value}

@router.delete("/{url_key}", status_code=204)
def delete_url(url_key: str, session: SessionDep):
    url = check_if_exists(url_key, session)

    session.delete(url)
    session.commit()
    return {"deleted url key": url_key}
