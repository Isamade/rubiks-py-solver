FROM python:3.15.0a8-slim-bookworm

WORKDIR /app

COPY ./requirements.txt ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "src/server.py"]