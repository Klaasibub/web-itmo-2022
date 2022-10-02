from concurrent.futures import ThreadPoolExecutor

import grpc

from builds.service_pb2 import AddReply
from builds.service_pb2_grpc import AddServiceServicer, add_AddServiceServicer_to_server


class Service(AddServiceServicer):
    def Health(self, request, context):
        return request

    def Add(self, request, context):
        return AddReply(result=(request.first + request.second))


def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_AddServiceServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:3000")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()
