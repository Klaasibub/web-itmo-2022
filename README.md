# web-itmo-2022

## Main project
*_Run command from project root_

Through docker-compose

1. Run docker-compose: `docker-compose up -d`

Go to `0.0.0.0:8000/docs`


---

## gRPC
To run the gRPC server and client, you need to install dependencies:
```
pip3 install -r requirements/grpc.txt
```

Next, from the "rpc" folder, run the server in one terminal:
```
python server.py
```
And run the client in another terminal:
```
python client.py
```
