import grpc
import SimpleService_pb2 as pb2
import SimpleService_pb2_grpc as pb2_grpc

if __name__ == "__main__":
    channel = grpc.insecure_channel("127.0.0.1:5555")
    stub = pb2_grpc.SimpleServiceStub(channel)

    while True:
        try:
            msg = pb2.Message(message=input())
            response = stub.GetServerResponse(msg)

            print(response)
            print(response.received)
            print(response.message)
        
        except KeyboardInterrupt:
            break