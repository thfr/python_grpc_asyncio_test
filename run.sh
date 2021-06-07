#!/bin/bash

export PYTHONPATH=$PWD:$PYTHONPATH
export GRPC_VERBOSITY="info"

SERVER_PORT=50051

# compile
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. --mypy_out=. ./activator.proto

# run service
python3 server.py $SERVER_PORT &
SERVER_PID=$!

# run test client
python3 client.py $SERVER_PORT

kill $SERVER_PID
