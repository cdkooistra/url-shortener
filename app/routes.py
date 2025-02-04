from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pyshorteners

router = APIRouter()

class Item(BaseModel):
    url: str

url_db = {}

def url_shortener(url: str) -> str:
    
    s = pyshorteners.Shortener()

    return s.tinyurl.short(url)


@router.get("/", status_code= 200)
def read_root():
    return JSONResponse({"keys": list(url_db.keys())}, status_code=200)

@router.post("/", status_code=201)
def shorten_url(item: Item):
    if not item.url.startswith("http"):
        raise HTTPException(status_code=400, detail="error: Invalid URL")

    shorten_url = url_shortener(item.url)
    url_db[shorten_url] = item.url
    return {"Short_url": shorten_url}



# @app.get("/")
# get keys, 200

# @app.post("/")
# post URL to shorten ->
# 201, id
# 400, error?

# @app.delete("/")
# 404 error?

# @app.get("/{url_id}")
# return redirect (301) to URL or 404 not found

# @app.put("/{url_id}")

# @app.delete("/{url_id}")