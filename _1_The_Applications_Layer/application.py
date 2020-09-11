import sys

sys.path.append("..")
from _4_The_Link_Layer.endnode import Endnode

from common.global_state_container import global_state_container

class Application(object): # this code runs on the user's PQC (personal quantum computer)
    def __init__(self, username = None):
        print("creating new application")
        self.quantum_internet = None
        self.username = username
        self.endnode = Endnode()
        self.endnode.parent_application = self

    def send_qubit(self, remote_user): # qubit here is the local Qubit object on EndnodeHardware.
        if self.quantum_internet:
            self.endnode.send_flag = True
            # self.quantum_internet.send_qubit(self.endnode.hardware.memory_qubit, self.username, remote_user)
            self.quantum_internet.request_link(self.username, remote_user) # the quantum internet will now make the link then notify the endnode to teleport.
        else:
            print("not connected to the quantum internet")

    def handle_qubit_received(self):
        print("application received qubit with state", 
            global_state_container.state.get_qubit_state(self.endnode.hardware.lower_qubit.id))

    def send_message(self, obj, msg):
        obj.handle_message(msg)
 
    def handle_message(self, msg):
        print("application received message")
        if msg['msg'] == "child endnode: Qubit received.":
            self.handle_qubit_received()
            return 1
        else:
            return -1
