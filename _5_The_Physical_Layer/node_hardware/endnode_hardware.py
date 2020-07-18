import sys
import math
import random
from qutip import *

sys.path.append("../..")
from _5_The_Physical_Layer.qubit_carriers.qubit import Qubit
print("imported Qubit object", Qubit)

from common.global_state_container import global_state_container

class EndnodeHardware(object):
    def __init__(self, parent_endnode, qubits=1):
        print("creating endnode hardware")
#         self.id = None
        self.parent_endnode = parent_endnode
        self.global_state = global_state_container.state
        self.qubit = Qubit(self)
        self.fiber = None                                          
#         self.memoryQubits = []

    def connect_fiber(self, fiber):
        print("connecting fiber")
        self.fiber = fiber

    def send_message(self, obj, msg):
        obj.handleMessage(msg)

    def handle_message(self, msg):
#         msg = msg.split('-')
#         # id of the sender
#         id = msg[0]
#         if msg[1] == "decohered":
#             # notify the link layer
#             msg2 = packLinkExpired(#specify which link expired#)
#             self.send_message(self.parent_endnode, msg2)
        pass

    def measure(self, qubit, basis = "01"):
        # https://inst.eecs.berkeley.edu/~cs191/fa14/lectures/lecture10.pdf
        rho = self.global_state.state
        # construct the projectors
        P0 = tensor([identity(2) for _ in range(qubit.Id)] + 
                    basis(2,0) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.Id + 1, int(math.log2(self.global_state.state.shape[0])))])
        P1 = tensor([identity(2) for _ in range(qubit.Id)] + 
                    basis(2,1) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.Id + 1, int(math.log2(self.global_state.state.shape[0])))])
        # compute the probabilities of the 1 and 0 outcomes
        p0 = (P0 * rho).tr()
        p1 = (P1 * rho).tr() # check that p1 = 1 - p0
        # choose an outcome at random using the probabilities above.
        result = 0 if random.random() < p0 else 1
        # simulate state collapse
        new_state = P0 * rho * P0 / p0 if result == 0 else P1 * rho * P1 / p1
        # update globalState
        self.global_state.update_state(new_state)
        # return the measurement result
        return result

    def load_qubit_on_photon(self, qubit, photon):  # both qubit and photon are qubit objects
        # swaps the state of the photon and the local qubit 
        # (the photon should be initialized to |0>. The initialization 
        # can be noisy).
        SWAP = swap(N=int(math.log2(self.global_state.state.shape[0])), targets=[qubit.id-1, photon.id-1])
        new_state = SWAP * self.global_state.state * SWAP.dag()
        self.global_state.update_state(new_state)

    def send_photon_through_fiber(self, photon, fiber):
        fiber.carry_photon(photon, self)

    def receive_photon_from_fiber(self, photon, fiber):
        print("endnode hardware receiving photon")
        # This function is called by an optical fiber to
        # alert the repeaterHardware to receive the incoming photon.
        # The repeaterHardware chooses a (physical) qubit on which to unload the 
        # qubit carried on the photon.
        self.unload_qubit_from_photon(self.qubit, photon) # confusing names.
        
    def unload_qubit_from_photon(self, qubit, photon):
        # swaps the state of the photon and the local qubit 
        # (the local qubit should be initialized to |0>. The initialization 
        # can be noisy). 
        SWAP = swap(N=int(math.log2(self.global_state.state.shape[0])), targets=[qubit.id-1, photon.id-1])
        new_state = SWAP * self.global_state.state * SWAP.dag()
        self.global_state.update_state(new_state)
        # notify the layers above that a qubit was received.
        msg = {'msg' : "received qubit",  # this is the standard. Document it somewhere.
               'sender' : self.fiber.node2 if self == self.fiber.node1 else self.fiber.node1, 
               'receiver' : self}
        if self.parent_endnode:
            self.send_message(self.parent_endnode, msg)

    def attempt_link_creation(self, remote_repeater):
        # remote is a repeater object.
        # here the physical details of link creation will be implemented:
        # 1. create EPR pair. Store one half locally and load the other on a photon.
        # 2. send the photon to the remote receiver.
        theQubit = self.leftQubit if self.parent_endnode.id > remote.id else self.qubit
        theOpticalFiber = self.leftOpticalFiber if self.parentEndnode.id > remote.id else self.rightOpticalFiber
        thePhoton = theOpticalFiber.photon12 if self.id > remote.id else theOpticalFiber.photon12
        self.load_qubit_on_photon(theQubit, thePhoton)
        self.send_photon_through_fiber(thePhoton, theOpticalFiber)
        # 3. (for later) check somehow that we have a good link.
        # support for heralding stations and photon transmission, etc.

    def attempt_distillation(self):
        # apply gates on the qubits here
        return
