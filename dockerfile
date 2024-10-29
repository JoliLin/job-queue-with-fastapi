FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY html/ ./html/
COPY jq/ ./jq/

EXPOSE 5566
EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn app.app:app --host 0.0.0.0 --port 5566 & python -m http.server --directory html 8080"]
