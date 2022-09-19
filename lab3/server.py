import sys
import threading

import zmq

client_output_msg = []
context = zmq.Context()
client_input_port = sys.argv[1]
client_output_port = sys.argv[2]


def client_inputs():
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{client_input_port}")

    while True:
        msg = socket.recv_string()
        print(f"input msg: {msg}")
        client_output_msg.append(msg)
        socket.send_string("ack")


def client_outputs():
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{client_output_port}")

    while True:
        if len(client_output_msg) != 0:
            print(f"send message {client_output_msg[0]}")
            socket.send_string(f"{client_output_msg[0]}")
            del client_output_msg[0]


client_input_thread = threading.Thread(target=client_inputs)
client_output_thread = threading.Thread(target=client_outputs)

client_input_thread.start()
client_output_thread.start()
