
import sys

sys.path.append("..")
from _5_The_Physical_Layer.opticalFiber.opticalFiber import OpticalFiber

class Cable(object):
    def __init__(self, node1, node2):
        self.id = None
        # node1 and node2 are repeater objects (link layer)
        self.node1 = node1
        self.node2 = node2
        self.optical_fiber = OpticalFiber(node1.repeater_hardware, node2.repeater_hardware) 
