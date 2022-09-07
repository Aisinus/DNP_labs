from socket import *
import sys
import os

address_host, port = sys.argv[1].split(":")
filename = sys.argv[2]
new_filename = sys.argv[3]
address = (address_host, port)
s = socket(AF_INET,SOCK_DGRAM)
s.settimeout(0.5)
seqn = 0
buff = 1024

file = open(filename, "rb")
file_bytes = file.read()
file_size = len(file_bytes)
check_connection = False

for i in range(1, 6):
    print(i)
    try:
        print("send start message " + address_host + ":" + port)
        msg = f"s | {seqn} | {new_filename} | {file_size}"
        s.sendto(msg.encode(), address)
        ack_msg = s.recvfrom(buff)[0]
        msg_type, seqn_next, buff = ack_msg.decode("utf-8").split(" | ")
        if msg_type != "a" or seqn_next != 1:
            raise Exception()
        check_connection = True
        break
    except:
        check_connection = False

if not check_connection:
    print("connection fail")
    sys.exit(0)
else:
    print("yeah")