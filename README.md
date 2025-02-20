# wscs

## Project Description

RESTful URL shortening service

## Installation Setup

Requires [Docker (Compose)](https://www.docker.com/):

```bash
mkdir secrets
openssl rand -hex 16 > secrets/db_pw
openssl rand -hex 32 > secrets/secret_key
```

## Usage

How to run (when in ./docker):

```bash
docker compose up -d
```

### References

Insperations for URL validation regex
[1] <https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/>
[2] <https://docs.netapp.com/us-en/oncommand-insight/config-admin/regular-expression-examples.html#formatting-regular-expressions>
