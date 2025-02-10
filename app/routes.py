from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import validators
from urllib.parse import urlsplit
import re
import hashlib

router = APIRouter()

class Item(BaseModel):
    """
    Item model representing a URL.

    Attributes:
        value (str): The URL string.
    """
    value: str
    
url_db = {}

def generate_id(url: str) -> str:
    """
    Generate a short identifier from the first three letters of the domain name.
    
    """
    parsed_url = urlsplit(url)  # Split URL to get essential parts

    domain = parsed_url.netloc.replace("www.", "")  # Remove 'www.' if present

    id = domain[:2]  # Take first three letters of domain to be the id
    hash_val = hashlib.md5(url.encode()).hexdigest()[:2]

    # hold = id
    # counter = 1
    # while id in url_db:
    #     print(counter)
    #     id = hold + str(counter)
    #     counter += 1

    return id + hash_val

def validate_url(url:str) -> bool:
    """
    Validate URL using regex
    """

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,10}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    
    pattern = re.compile(regex)
    return bool(re.fullmatch(pattern, url))    

@router.get("/", status_code = 200)
def list_keys():
    return JSONResponse({"keys": list(url_db.keys())}, status_code=200)

@router.post("/", status_code = 201)
def shorten_url(item: Item):
    
    if not validators.url(item.value):
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    shorten_url = generate_id(item.value)
    url_db[shorten_url] = item.value
    return {"id": shorten_url}

@router.delete("/" , status_code = 404) 
def delete_nothing():
    raise HTTPException(status_code = 404, detail = "error: Not Supported (No ID)")


@router.get("/{url_key}", status_code=301)
def redirect_url(url_key: str):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    return JSONResponse(status_code=301, content={"value": url_db[url_key]})


@router.put("/{url_key}", status_code=200)
async def update_url(url_key: str, request: Request):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")

    body = await request.json() # get the request body encoded in json

    new_url = body.get("url") # get the url from request body 

    if not new_url or not validate_url(new_url): 
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    url_db[url_key] = new_url
    return {"updated url key": url_key}

@router.delete("/{url_key}", status_code=204)
def delete_url(url_key: str):
    if url_key not in url_db:
        raise HTTPException(status_code=404, detail="error: URL not found")
    
    del url_db[url_key]
    return {"deleted url key": url_key}
