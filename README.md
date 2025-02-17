# wscs

## Project Description

RESTful URL shortening service

## Installation Setup

Requires python 3.9+

Install requirements: pip install -r requirements.txt

How to run app/auth (specify separate port for app and auth agent):

```bash
uvicorn app.main:app --reload --port [PORT]
uvicorn auth.main:app --reload --port [PORT]
```

How to run (Windows):

```bash
fastapi dev main.py
```

### References

Insperations for URL validation regex
[1] <https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/>
[2] <https://docs.netapp.com/us-en/oncommand-insight/config-admin/regular-expression-examples.html#formatting-regular-expressions>
