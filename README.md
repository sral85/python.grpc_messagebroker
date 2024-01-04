# Message Broker based on gRPC

First install all relevant third party packages

``` 
pip install -r requirements.txt
```

```
python3 -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/messagebroker.proto
```

```
python3 server.py
```