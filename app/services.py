from urllib.parse import urlsplit
import re
import hashlib

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

    return str(id + hash_val)

def validate_url(url:str) -> bool:
    """
    Validate URL using regex
    """

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,10}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&'//=\\-–]*)")
    
    pattern = re.compile(regex)
    return bool(re.fullmatch(pattern, url))    
