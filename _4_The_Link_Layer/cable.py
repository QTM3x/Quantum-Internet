import sys

sys.path.append("..")
from _5_The_Physical_Layer.optical_fiber.optical_fiber import OpticalFiber
print("imported OpticalFiber object", OpticalFiber)

class Cable(object):
    def __init__(self):
        print("creating new cable")
        self.id = None
        # node1 and node2 are repeater objects (link layer)
        self.node1 = None
        self.node2 = None
        self.optical_fiber = OpticalFiber()

    def is_connected(self, node):
        return node == self.node1 or node == self.node2

    def connect_node(self, node):
        if self.node1 is None:
            self.node1 = node
            self.optical_fiber.connect_node_hardware(node.hardware, pos=1)
        else:
            self.node2 = node
            self.optical_fiber.connect_node_hardware(node.hardware, pos=2)
