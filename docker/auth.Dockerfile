FROM python:3.12-slim

WORKDIR /auth
COPY ./auth /auth/auth
COPY ./requirements.txt /auth/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "auth.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
