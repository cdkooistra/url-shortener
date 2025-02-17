from auth.utils import b64_encode, b64_decode, sha256, hmac
from datetime import datetime, timedelta
from typing import Union
import json
import os

def create_jwt(payload: dict) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    header_enc = b64_encode(json.dumps(header).encode())

    payload["exp"] = (datetime.now() + timedelta(minutes=int(os.environ.get("TOKEN_EXPIRATION_MINUTES")))).timestamp()
    payload_enc = b64_encode(json.dumps(payload).encode()) 

    signature = hmac.new(os.environ.get("SECRET").encode(), f"{header_enc}.{payload_enc}".encode(), sha256).digest()
    signature_enc = b64_encode(signature)

    return f"{header_enc}.{payload_enc}.{signature_enc}"

def verify_jwt(token: str) -> Union[dict, bool]:
    header_enc, payload_enc, signature_enc = token.split(".")
    expected_signature = hmac.new(os.environ.get("SECRET").encode(), f"{header_enc}.{payload_enc}".encode(), sha256).digest()

    if not hmac.compare_digest(b64_encode(expected_signature), signature_enc):
        return False
    
    payload = json.loads(b64_decode(payload_enc).decode())
    if datetime.now().timestamp() > payload.get("exp",0):
        return False
    
    return payload # either return False or return payload. Error handling not in this file but in routes.py
