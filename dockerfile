FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS app1

COPY app/ ./app/
COPY html/ ./html/
COPY jq/ ./jq/
COPY test/ ./test/

CMD ["sh", "-c", "python app/app.py"]

FROM base AS app2

COPY app/ ./app/
COPY html/ ./html/

CMD ["sh", "-c", "python app/app_web.py"]
