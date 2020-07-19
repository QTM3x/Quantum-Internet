import sys

sys.path.append("..")
from _4_The_Link_Layer.endnode import Endnode

class Application(object): # this code runs on the user's PQC (personal quantum computer)
    def __init__(self, username = None):
        print("creating new application")
        self.quantum_internet = None
        self.username = username
        self.endnode = Endnode()
        self.endnode.parent_application = self

    def send_qubit(self, qubit, remote_user):
        self.quantum_internet.send_qubit(qubit, self.username, remote_user)

    def receive_qubit(self, qubit):
        pass
