
class Link(object):
    def __init__(self, node1, node2, fidelity):
        # Each node is a repeater object
        self.node1 = node1
        self.node2 = node2
        self.fidelity = fidelity
