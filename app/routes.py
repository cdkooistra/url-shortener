from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}



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
