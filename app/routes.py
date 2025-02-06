from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pyshorteners
import validators

router = APIRouter()

class Item(BaseModel):
    """
    Item model representing a URL.

    Attributes:
        url (str): The URL string.
    """
    url: str

url_db = {}

def url_shortener(url: str) -> str:
    
    s = pyshorteners.Shortener()

    return s.tinyurl.short(url)



@router.get("/", status_code= 200)
def list_keys():
    return JSONResponse({"keys": list(url_db.keys())}, status_code=200)

@router.post("/", status_code=201)
def shorten_url(item: Item):
    if not validators.url(item.url):
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    shorten_url = url_shortener(item.url)
    url_db[shorten_url] = item.url
    return {"Short_url": shorten_url}


@router.get("/{url_key}", status_code=301)
def redirect_url(url_key: str):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    return JSONResponse(status_code=301, content={"Location": url_db[url_key]})


@router.put("/{url_key}", status_code=200)
def update_url(url_key: str, item: Item):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    # catch any other exception for return code 400? "error"

    url_db[url_key] = item.url
    return {"updated url key": url_key}

@router.delete("/{url_key}", status_code=204)
def delete_url(url_key: str):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    del url_db[url_key]
    return {"deleted url key": url_key}
