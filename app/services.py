from urllib.parse import urlsplit
import re
import hashlib
import requests
import os

def generate_id(url: str) -> str:
    """
    Generate a short identifier from the first three letters of the domain name.
    
    """
    parsed_url = urlsplit(url)  # Split URL to get essential parts

    domain = parsed_url.netloc.replace("www.", "")  # Remove 'www.' if present

    id = domain[:2]  # Take first three letters of domain to be the id
    hash_val = hashlib.md5(url.encode()).hexdigest()[:2]

    return str(id + hash_val)

def validate_url(url:str) -> bool:
    """
    Validate URL using regex
    """

    regex = ("((http|https)://)(www.)?" + # for 'http://' or 'https://' and optionally www.
             "([a-zA-Z0-9.-]+)" +  # for a variety of domain names (letters, numbers, dots, etc,)
             "(\.[a-zA-Z]{2,10}([-a-zA-Z0-9@:%._\\+~#?&/=]*)?)" + # for domain extensions (.com, .org, etc.)
             "(/.*)?$") # for path/query string 
    
    pattern = re.compile(regex)
    return bool(re.fullmatch(pattern, url))    

# Call verification on the Auth sercvice
def verify_token(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{os.getenv("AUTH_URL")}/users/verify", headers=headers)
    
    if response.status_code != 200:
        return None  # Invalid token

    return response.json()  # Returns the payload (e.g., {"sub": "username"})