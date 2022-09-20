import sys
import threading
import zmq

client_output_msg = []
context = zmq.Context()
client_input_port = sys.argv[1]
client_output_port = sys.argv[2]
worker_input_port = sys.argv[3]
worker_output_port = sys.argv[4]


def client_inputs():
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{client_input_port}")

    while True:
        msg = socket.recv_string()
        print(f"input msg: {msg}")
        client_output_msg.append(msg)
        socket.send_string("ack")
        worker_input(msg)


def client_outputs():
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{client_output_port}")

    while True:
        if len(client_output_msg) != 0:
            print(f"send message {client_output_msg[0]}")
            socket.send_string(f"{client_output_msg[0]}")
            del client_output_msg[0]


pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{worker_input_port}")

def worker_input(_msg):
    pub_socket.send_string(_msg)

def worker_output():
    sub_socket = context.socket(zmq.SUB)
    sub_socket.subscribe("")
    sub_socket.bind(f"tcp://127.0.0.1:{worker_output_port}")
    while True:
        try:
            res = sub_socket.recv_string()
            print(f"{res}")
            client_output_msg.append(res)
        except Exception as e:
            print(e)

client_input_thread = threading.Thread(target=client_inputs)
client_output_thread = threading.Thread(target=client_outputs)
worker_output_thread = threading.Thread(target=worker_output)

client_input_thread.start()
client_output_thread.start()
worker_output_thread.start()