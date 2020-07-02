%load_ext autoreload
%autoreload 2

from ../4_The_Link_Layer import repeater cable
import globalState

class repeaterChain(object):
    def __init__(self, length):
        self.length = length
        self.repeaters = [repeater(self) for i in range(length)]
#         self.connectedEndnodes = []
        # connect the repeaters with cables
        for i in range(length):
            # for every repeater create a new cable to the right
            if i < length-1:
                self.repeaters[i].rightCable = cable(self.repeaters[i], self.repeaters[i+1])
            if i > 0:
                self.repeaters[i].leftCable = self.repeaters[i-1].rightCable

    def attemptSwap(self, repeater):
        #ask repeater to do a swap
        repeater.attemptSwap(#specify the links to swap#)

    def attemptLinkCreation(self, repeater1, repeater2):
        repeater1.attemptLinkCreation(repeater2)

    def connect(self, endnode): #endnode is a link layer object
        if self.repeaters[0].leftCable == None: # in the future choose where to connect in a better way
            endnode.cable = cable(endnode, self.repeaters[0])
            self.repeaters[0].leftCable = endnode.cable
        else:
            self.repeaters[self.length-1].rightCable = cable(self.repeaters[self.length-1], endnode)
            endnode.cable = self.repeaters[self.length-1].rightCable
        self.assignNetworkId(endnode)

    def assignNetworkId(self, node):
        if type(node) == "endnode":
            if node.cable == None:
                print("endnode is not wired to network.")
            elif node.cable == self.repeaters[0].leftCable:
                node.netId = 0
            elif node.cable == self.repeaters[self.length-1].rightCable:
                node.netId = self.length
        elif type(node) == "repeater":
            if node.rightCable == None and node.leftCable == None:
                print("repeater is not wired to network")
            else:
                node.netId = self.repeaters.index(node) + 1
        else:
            print("unknown node type.")
