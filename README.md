# wscs

## Project Description

RESTful URL shortening service

## Installation Setup

Requires [Docker (Compose)](https://www.docker.com/):
Requires [OpenSSL](https://openssl.org/):

```bash
mkdir secrets
openssl rand -hex 16 > secrets/db_pw
openssl rand -hex 32 > secrets/secret_key
```

For windows users, run:
```bash
(Get-Content ../secrets/db_pw) | Set-Content -NoNewline ../secrets/db_pw
(Get-Content ../secrets/secret_key) | Set-Content -NoNewline ../secrets/secret_key
```

## Usage

How to run (when in ./docker):

```bash
docker compose up -d

```


### Set up for Kubernetes

```
DB_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)

kubectl create secret generic app-secrets \
  --from-literal=db_pw="$DB_PASSWORD" \
  --from-literal=secret_key="$SECRET_KEY"

```

### References

Inspirations for URL validation regex
[1] <https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/>
[2] <https://docs.netapp.com/us-en/oncommand-insight/config-admin/regular-expression-examples.html#formatting-regular-expressions>
