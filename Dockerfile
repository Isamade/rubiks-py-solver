FROM python:3.15.0a8-slim-bookworm

WORKDIR /app

COPY ./requirements.txt ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

COPY . .

# Generate protobuf files
RUN mkdir -p ./src/generated && \
    python -m grpc_tools.protoc -I./proto --python_out=./src/generated --grpc_python_out=./src/generated ./proto/solver.proto

CMD ["python", "-u", "src/server.py"]