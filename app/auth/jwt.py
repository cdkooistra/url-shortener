# JWT logic here
from utils import b64_encode, b64_decode, sha256, json
import os

def create_jwt(payload: dict) -> str:
    # create a JWT token using the payload and secret
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    header = b64_encode(json.dumps(header).encode())

    # TODO: Unsure what to do with the payload

    signature = sha256(header + "." + payload, os.environ.get("SECRET")).hexdigest()

    return f"{header}.{payload}.{signature}"


def verify_jwt(token: str) -> bool:
    # verify the JWT token using the secret
    header, payload, signature = token.split(".")

    expected_signature = sha256(header + "." + payload, os.environ.get("SECRET")).hexdigest()

    if expected_signature is not signature:
        return False
    else: 
        return True
