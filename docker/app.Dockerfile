FROM python:3.12-slim

WORKDIR /app
COPY ./app /app/app
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
