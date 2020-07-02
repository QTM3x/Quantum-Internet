%load_ext autoreload
%autoreload 2

from ../5_The_Physical_Layer import opticalFiber

class cable(object):
    def __init__(self, node1, node2):
        self.id = None
        # node1 and node2 are repeater objects (link layer)
        self.node1 = node1
        self.node2 = node2
        self.opticalFiber = opticalFiber(node1.repeaterHardware, node2.repeaterHardware) 
