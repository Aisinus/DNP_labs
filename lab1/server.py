import sys
from socket import *

class Client:
    def __init__(self, seqn, filename, size):
        self.seqn = seqn
        self.init_seqn = seqn
        self.filename = filename
        self.size = size
        self.data = None

    def set_seqno(self, seqn):
        self.seqn = seqn

    def add_data(self, new_data):
        if self.data is None:
            self.data = new_data
        else:
            self.data += new_data


port = int(sys.argv[1])
localhost = "localhost"
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(15)
s.bind((localhost, port))

while True:
    data, address_client = s.recvfrom(1024)
    print(f"{data} {address_client}")

