import sys
import threading
import zmq

sub_port = sys.argv[1]
pub_port = sys.argv[2]
context = zmq.Context()


def is_prime(n):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for divisor in range(3, n, 2):
        if n % divisor == 0:
            return False
    return True

def pub_result(number):
    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect(f"tcp://127.0.0.1:{pub_port}")
    if(is_prime(number)):
        print()
        pub_socket.send_string(f"{number} is prime")
    else:
        print()
        pub_socket.send_string(f"{number} is not prime")
    pub_socket.close()


sub = context.socket(zmq.SUB)
sub.subscribe("isprime")
sub.connect(f"tcp://localhost:{sub_port}")

while True:
    try:
        num = sub.recv_string()
        number = num.split(" ")[1]
        number = int(number)
        pub_result(number)
    except Exception as e:
        print(e)