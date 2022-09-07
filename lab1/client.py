from socket import *
import sys
import os

address_host, port = sys.argv[1].split(":")
port = int(port)
filename = sys.argv[2]
new_filename = sys.argv[3]
address = (address_host, port)
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(0.5)
seqn = 0
buff = 1024

file_size = os.path.getsize(filename)
check_connection = False

for i in range(1, 6):
    print(i)
    try:
        print(f"send start message {address}")
        msg = f"s | {seqn} | {new_filename} | {file_size}"
        s.sendto(msg.encode(), address)
        ack_msg = s.recvfrom(buff)[0]
        msg_type, seqn_next, buff = ack_msg.decode("utf-8").split(" | ")
        if msg_type != "a" or seqn_next != seqn + 1:
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

file = open(filename, "rb")
buff = int(buff)
seqn += 1
while True:
    try:
        msg = f"d | {seqn} | ".encode()
        data_bytes = file

    except:
        sys.exit(1)
