import grpc

from builds.service_pb2 import Null, AddArgs
from builds.service_pb2_grpc import AddServiceStub


def main():
    with grpc.insecure_channel("localhost:3000") as channel:
        client = AddServiceStub(channel)
        client.Health(Null())

        first = 1
        second = 41

        response = client.Add(AddArgs(
            first=first,
            second=second,
        ))

        print(f"Sum of {first} and {second} is equal to: ", response.result)


if __name__ == "__main__":
    main()
