import sys

sys.path.append("..")
from _4_The_Link_Layer.repeater import Repeater
print("imported Repeater object", Repeater)
from _4_The_Link_Layer.cable import Cable
print("imported Cable object", Cable)
# import globalState

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
        repeater.attempt_swap() #specify the links to swap#

#     def attempt_link_creation(self, repeater1, repeater2):
#         # this works between adjacent repeaters only. We don't want that. 
#         repeater1.attempt_link_creation(repeater2)
        
    def attempt_link_creation(self, endnode1, endnode2):
        # Here come the different network layer protocols.
        # 1. ask the repeaters to create links according to the protocol.
        # Simple protocol: ask all repeaters to create links at once.
        for i in range(len(self.repeaters)-1):
            self.repeaters[i].attempt_link_creation(self.repeaters[i+1])
        # Also ask the link layer for links between the endnodes and the
        # edge repeaters.
        # First we get the repeater wired to each endnode
        endnode1_repeater = self.repeaters[0] if endnode1.cable == self.repeaters[0].left_cable else self.repeaters[-1]
        endnode2_repeater = self.repeaters[0] if endnode2.cable == self.repeaters[0].left_cable else self.repeaters[-1]
        # Then we link them.
        endnode1.attempt_link_creation(endnode1_repeater)
        endnode2.attempt_link_creation(endnode2_repeater)
        # Then we swap.
        for i in range(len(self.repeaters)):
            self.repeaters[i].attempt_swap(self.repeaters[i].left_link, self.repeaters[i].right_link)
        # 2. once the link between the endnodes has been established, 
        #    notify quantum internet.

    def handle_endnodes_linked(self, endnode1, endnode2):
        msg = {'msg': "endnodes linked",
               'endnode1': endnode1,
               'endnode2': endnode2}
        self.send_message(self.parent_quantum_internet, msg)

    def assign_networkId(self, node):
        if type(node).__name__ == "Endnode":
            if node.cable == None:
                print("endnode is not wired to network.")
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
        if msg['msg'] == "repeater: swap complete":
            if type msg['node1'] == "Endnode" and type msg['node2'] == "Endnode":
                msg = {'msg': "network layer: Link to remote endnode created.",
                       'endnode1': msg['node1'],
                       'endnode2': msg['node2']}
                self.send_message(self.parent_quantum_internet, msg)
