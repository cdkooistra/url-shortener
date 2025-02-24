from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
import hmac

# i should probably start using docstrings for these comments

def b64_encode(data: bytes) -> str:
    # Helper function to encode bytes into base64 encoded strings.
    # We need to use urlsafe_b64encode as per JWT convention.
    # Also keep in mind to remove the '=' characters, as they are not allowed in urlsafe encoding, also as per JWT convention.
    
    return urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def b64_decode(data: str) -> bytes:
    # Helper function to decode base64 encoded strings.
    # We need to use urlsafe_b64decode as per JWT convention.
    # Also keep in mind to readd the '=' characters, as we remove them in the encoding step.
    padding = '=' * (4 - len(data) % 4)
    return urlsafe_b64decode(data + padding)

# TODO: we only save hashed passwords in our db, this is best practice
def hash_password(password: str) -> str:
    # Helper function to hash the password using sha256.
    return sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    #Verifies a password against the stored hash
    return hash_password(password) == hashed_password

def read_secret(secret):
    # Read Docker secret from file system
    secret_path = f"/run/secrets/{secret}"

    try:
        with open(secret_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
