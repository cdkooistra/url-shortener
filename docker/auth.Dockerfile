FROM python:3.12-slim

WORKDIR /auth
COPY ./auth /auth/auth
COPY ./requirements.txt /auth/
RUN apt update && apt install -y curl net-tools procps iputils-ping
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8001

CMD ["uvicorn", "auth.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
