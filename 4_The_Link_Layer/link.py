%load_ext autoreload
%autoreload 2

class link(object):
    def __init__(node1, node2, fidelity):
        # Each node is a repeater object
        self.node1 = node1
        self.node2 = node2
        self.fidelity = fidelity
