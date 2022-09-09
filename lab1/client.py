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
s.bind(("localhost", 0))
seqn = 0
buff = 1024

file_size = os.path.getsize(filename)
check_connection = False

for i in range(5):
    print(i + 1)
    try:
        print(f"send start message {address[0]}:{address[1]}")
        msg = f"s | {seqn} | {new_filename} | {file_size}"
        s.sendto(msg.encode(), address)
        ack_msg = s.recvfrom(buff)[0]
        msg_type, seqn_next, buff = ack_msg.decode().split(" | ")
        seqn_next = int(seqn_next)
        buff = int(buff)
        if msg_type != "a" or seqn_next != seqn + 1 or buff <= 0:
            checks = (msg_type != "a")
            checks2 = (seqn_next != seqn+1)
            checks3 = (buff<=0)
            print(f"{checks} {checks2} {checks3} {msg_type} {seqn} {seqn_next} {buff}")
            raise Exception()
        check_connection = True
        break
    except timeout:
        check_connection = False

if not check_connection:
    print("connection fail")
    sys.exit(0)
else:
    print("connected successfully")

file = open(filename, "rb")
seqn += 1
seqn_next = 0
while True:
    msg = f"d | {seqn} | ".encode()
    msg_pref = len(msg)
    data_bytes = file.read(buff - msg_pref)
    if data_bytes == b'':
        print("File transferred")
        break
    msg += data_bytes
    for i in range(5):
        try:
            print(f"try {i + 1}, seq number = {seqn}")
            s.sendto(msg, address)
            ack_msg = s.recvfrom(buff)[0]
            msg_type, seqn_next = ack_msg.decode().split(" | ")
            if msg_type != "a" or int(seqn_next) != seqn + 1:
                raise Exception()
            check_connection = True
            break
        except timeout:
            check_connection = False

    if not check_connection:
        print("Server did not respond 5 times or respond incorrect seq number or message type")
        break

    seqn = int(seqn_next)

s.close()
file.close()