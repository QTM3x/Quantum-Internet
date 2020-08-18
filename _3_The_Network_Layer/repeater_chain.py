import sys

sys.path.append("..")
from _4_The_Link_Layer.repeater import Repeater
from _4_The_Link_Layer.cable import Cable

from .Protocols.link_creation.example_protocol_1 import ExampleProtocol1

class RepeaterChain(object):
    def __init__(self, length, parent_quantum_internet):
        print("creating new repeater chain")
        self.length = length
        self.repeaters = [Repeater(self) for i in range(length)]
        self.parent_quantum_internet = parent_quantum_internet
#         self.connectedEndnodes = []
        # connect the repeaters with cables
        for i in range(length):
            # for every repeater create a new cable to the right
            if i < length-1:
                new_cable = Cable()
                self.repeaters[i].connect_right_cable(new_cable)
            if i > 0:
                self.repeaters[i].connect_left_cable(self.repeaters[i-1].right_cable)
            # after a repeater is connected, let the network
            # layer give it a network Id.
            self.assign_networkId(self.repeaters[i])
            print("assigned net id", self.repeaters[i].netId)
        self.protocol = ExampleProtocol1(self)

    def connect(self, endnode): #endnode is a link layer object
        print("connecting endnode to repeater chain")
        if self.repeaters[0].left_cable == None: # in the future choose where to connect in a better way
            new_cable = Cable()
            endnode.connect_cable(new_cable)
            self.repeaters[0].connect_left_cable(new_cable)
        else:
            new_cable = Cable()
            self.repeaters[self.length-1].connect_right_cable(new_cable) 
            endnode.connect_cable(new_cable)
        self.assign_networkId(endnode)
        print("assigned net id", endnode.netId)

    def attempt_swap(self, repeater):
        #ask repeater to do a swap
        repeater.attempt_swap(repeater.left_link, repeater.right_link) #specify the links to swap#

#     def attempt_link_creation(self, repeater1, repeater2):
#         # this works between adjacent repeaters only. We don't want that. 
#         repeater1.attempt_link_creation(repeater2)
        
    def request_link(self, endnode1, endnode2, minimum_fidelity=-1):
        print("handling link request in repeater chain")
        # Here come the different network layer protocols.
        msg = {'msg' : "network layer: Link request received.",
               'endnode1' : endnode1,
               'endnode2' : endnode2,
               'minimum_fidelity' : minimum_fidelity
               }
        self.send_message(self.protocol, msg)

    # def handle_endnodes_linked(self, endnode1, endnode2):
    #     msg = {'msg': "repeater chain: Endnodes linked.",
    #            'endnode1': endnode1,
    #            'endnode2': endnode2}
    #     self.send_message(self.parent_quantum_internet, msg)

    def assign_networkId(self, node):
        if type(node).__name__ == "Endnode":
            if node.cable == None:
                print("endnode is not wired to network")
            elif node.cable == self.repeaters[0].left_cable:
                node.netId = 0
            elif node.cable == self.repeaters[-1].right_cable:
                node.netId = self.length + 1
        elif type(node).__name__ == "Repeater":
            if node.right_cable == None and node.left_cable == None:
                print("repeater is not wired to network")
            else:
                node.netId = self.repeaters.index(node) + 1
        else:
            print("unknown node type.")

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        print("repeater chain received message")
        if msg['msg'] == "repeater: Swap complete.":
            if type(msg['node1']).__name__ == "Endnode" and type(msg['node2']).__name__ == "Endnode":
                msg = {'msg': "network layer: Link to remote endnode created.",
                       'endnode1': msg['node1'],
                       'endnode2': msg['node2']}
                self.send_message(self.parent_quantum_internet, msg)
        else:
            print("repeater chain received unknown message \"" + msg['msg'] + "\"")
