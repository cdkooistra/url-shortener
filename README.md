# URL Shortener

## Project Description

This is a URL shortener API created for a Master's course at the University of Amsterdam (UvA). The course introduces students to the design and usage of cloud architectures. This development project specifically gives hands-on experience in designing and deploying a microservices architecture, while also keeping in mind of modern practices for application security, scalability, and deployment in real-world cloud environments.

## Installation setup (Docker)

Requires [Docker (Compose)](https://www.docker.com/) and [OpenSSL](https://openssl.org/):

```bash
mkdir secrets
openssl rand -hex 16 > secrets/db_pw
openssl rand -hex 32 > secrets/secret_key
```

**Windows users** might have to run:

```bash
(Get-Content ../secrets/db_pw) | Set-Content -NoNewline ../secrets/db_pw
(Get-Content ../secrets/secret_key) | Set-Content -NoNewline ../secrets/secret_key
```

### Usage

How to run (when in ./docker):

```bash
docker compose up -d
```

## Installation setup (Kubernetes)

Created secret folder within the virtual machine:

```bash
DB_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)

kubectl create secret generic app-secrets \
  --from-literal=db_pw="$DB_PASSWORD" \
  --from-literal=secret_key="$SECRET_KEY"

```

### References

[1] <https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/>

[2] <https://docs.netapp.com/us-en/oncommand-insight/config-admin/regular-expression-examples.html#formatting-regular-expressions>
