import sys

sys.path.append("..")
from _4_The_Link_Layer.repeater import Repeater
print("imported Repeater object", Repeater)
from _4_The_Link_Layer.cable import Cable
print("imported Cable object", Cable)
# import globalState

class RepeaterChain(object):
    def __init__(self, length):
        print("creating new repeater chain")
        self.length = length
        self.repeaters = [Repeater(self) for i in range(length)]
#         self.connectedEndnodes = []
        # connect the repeaters with cables
        for i in range(length):
            # for every repeater create a new cable to the right
            if i < length-1:
                new_cable = Cable(self.repeaters[i], self.repeaters[i+1])
                self.repeaters[i].connect_right_cable(new_cable)
            if i > 0:
                self.repeaters[i].connect_left_cable(self.repeaters[i-1].right_cable)
            # after a repeater is connected, let the network
            # layer give in a network Id.
            self.assign_networkId(self.repeaters[i])
            print("assigned net id", self.repeaters[i].netId)

    def attempt_swap(self, repeater):
        #ask repeater to do a swap
        repeater.attempt_swap() #specify the links to swap#

    def attempt_link_creation(self, repeater1, repeater2):
        repeater1.attempt_link_creation(repeater2)

    def connect(self, endnode): #endnode is a link layer object
        print("connecting endnode to repeater chain")
        if self.repeaters[0].left_cable == None: # in the future choose where to connect in a better way
            new_cable = Cable(endnode, self.repeaters[0])
            endnode.connect_cable(new_cable) 
            self.repeaters[0].connect_left_cable(new_cable)
        else:
            new_cable = cable(self.repeaters[self.length-1], endnode)
            self.repeaters[self.length-1].connect_right_cable(new_cable) 
            endnode.connect_cable(new_cable)
        self.assign_networkId(endnode)

    def assign_networkId(self, node):
        if type(node).__name__ == "EndNode":
            if node.cable == None:
                print("endnode is not wired to network.")
            elif node.cable == self.repeaters[0].left_cable:
                node.netId = 0
            elif node.cable == self.repeaters[self.length-1].right_cable:
                node.netId = self.length
        elif type(node).__name__ == "Repeater":
            if node.right_cable == None and node.left_cable == None:
                print("repeater is not wired to network")
            else:
                node.netId = self.repeaters.index(node) + 1
        else:
            print("unknown node type.")
