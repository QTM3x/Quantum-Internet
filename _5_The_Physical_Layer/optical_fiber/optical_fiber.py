
import sys

sys.path.append("..")
from common.global_state_container import global_state_container
from _5_the_physical_layer import photon

class OpticalFiber(object):
    def __init__(self, node1, node2, length=1):
        self.global_state = global_state_container.state
#         self.id = None
        # The length of the fiber.
        self.length = length
        # The two nodes at the two ends of the fiber.
        # A node can be a repeaterHardware, an end node, a heralding station, 
        # etc. For now it's a repeaterHardware object for simplicity.
        self.node1 = node1
        self.node2 = node2
        self.photon12 = photon.Photon(self)   # this is the photon going from node 1 to node 2
        self.photon21 = photon.Photon(self)

    def carry_photon(self, photon, sender, receiver):  # Here there will be a quantum channel applied to the state
        # apply channel here
        # for now make it the identity channel
        gate = tensor([identity(2) for _ in range(self.global_state.N)])
        new_state = gate * self.global_state.state * gate.dag()  # for now the map is a identity unitary gate
        self.global_state.update_state(new_state)
        # send output state to the receiver
        receiver.receive_photon()
