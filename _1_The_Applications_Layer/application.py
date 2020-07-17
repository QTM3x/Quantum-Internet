import sys

sys.path.append("..")
from _4_The_Link_Layer.endnode import Endnode

class Application(object): # this code runs on the user's PQC (personal quantum computer)
    def __init__(self, username = None):
        print("creating new application")
        self.quantum_internet = None
        self.username = username
        # endnode is the node the application is running on
        self.endnode = Endnode() 

    def send_qubit(qubit, remote_user):
        # check if we have a link with receiverId
        # if we don't have one, request one
        self.quantum_intenet.request_link("Bob")
        # send the classical bits to Bob
#         qInternet.text("Bob", "bits are " + ...)
