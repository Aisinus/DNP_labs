import sys
import threading
import zmq

req_port = sys.argv[1]
sub_port = sys.argv[2]
context = zmq.Context()

req = context.socket(zmq.REQ)
req.connect(f"tcp://localhost:{req_port}")


def send_msg(msg):
    if msg == "":
        return True
    try:
        req.send_string(msg)
        response = req.recv_string()
        if response == "ack":
            return True
        return False
    except TimeoutError:
        return False


def accept_msg():
    sub = context.socket(zmq.SUB)
    sub.subscribe("")
    sub.connect(f"tcp://localhost:{sub_port}")
    while True:
        try:
            _msg = sub.recv_string()
            print(f"{_msg}")
        except Exception as e:
            print(e)


sub_thread = threading.Thread(target=accept_msg)
sub_thread.start()

while True:
    msg = input()
    if not send_msg(msg):
        break

sys.exit(1)
