import sys
import math
from qutip import *

sys.path.append("..")
from common.global_state_container import global_state_container
from ..qubit_carriers.photon import Photon

class OpticalFiber(object):
    def __init__(self, length=1):
        print("creating new optical fiber")
        self.global_state = global_state_container.state
#         self.id = None
        # The length of the fiber.
        self.length = length
        # The two nodes at the two ends of the fiber.
        # A node can be a repeaterHardware, an end node, a heralding station, 
        # etc. For now it's a repeaterHardware object for simplicity.
        self.node1 = None
        self.node2 = None
#         self.photon12 = Photon(self)   # this is the photon going from node 1 to node 2
#         self.photon21 = Photon(self)

    def connect_node_hardware(self, node_hardware, pos=None):
        if pos == 1:
            self.node1 = node_hardware
        elif pos == 2:
            self.node2 = node_hardware
        else:
            if self.node1 is None:
                self.node1 = node_hardware
            else:
                self.node2 = node_hardware

    def carry_photon(self, photon, sender):  # Here there will be a quantum channel applied to the state
        # sender is a node hardware object.
        # apply channel here
        # for now make it the identity channel
        gate = tensor([identity(2) for _ in range(int(math.log2(self.global_state.state.shape[0])))])
        new_state = gate * self.global_state.state * gate.dag()  # for now the map is a identity unitary gate
        self.global_state.update_state(new_state)
        # send output state to the receiver
        receiver = self.node2 if sender == self.node1 else self.node1
        receiver.receive_photon_from_fiber(photon, self)
