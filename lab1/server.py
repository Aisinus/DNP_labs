import sys

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


socket = sys.argv[1]
