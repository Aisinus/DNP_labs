from math import gcd
import sys
import threading
from tokenize import Double
import zmq

sub_port = sys.argv[1]
pub_port = sys.argv[2]
context = zmq.Context()



def pub_result(number1, number2):
    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect(f"tcp://127.0.0.1:{pub_port}")
    print()
    pub_socket.send_string(f"gcd for {number1} {number2} is {gcd(number1, number2)}")
    pub_socket.close()


sub = context.socket(zmq.SUB)
sub.subscribe("gcd")
sub.connect(f"tcp://localhost:{sub_port}")

while True:
    try:
        num = sub.recv_string()
        firstnum = int(num.split(" ")[1])
        secondnum = int(num.split(" ")[2])
        pub_result(firstnum, secondnum)
    except Exception as e:
        pass
        print(e)