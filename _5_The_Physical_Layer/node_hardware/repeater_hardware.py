import sys
import math
import random
from qutip import *

sys.path.append("../..")
from _5_The_Physical_Layer.qubit_carriers.qubit import Qubit
print("imported Qubit object")
from _5_The_Physical_Layer.qubit_carriers.photon import Photon
print("imported Photon object")

from common.global_state_container import global_state_container

class RepeaterHardware(object):
    def __init__(self, parent_repeater, qubits=2):
        print("creating new repeater hardware")
        self.parent_repeater = parent_repeater
        self.global_state = global_state_container.state
        self.left_qubit = Qubit(self)
        self.right_qubit = Qubit(self)
        self.left_fiber = None
        self.right_fiber = None                                         
#         self.memoryQubits = []

    def connect_right_fiber(self, fiber):
        print("connecting right optical fiber")
        self.right_fiber = fiber
        fiber.connect_node_hardware(self)

    def connect_left_fiber(self, fiber):
        print("connecting left optical fiber")
        self.left_fiber = fiber
        fiber.connect_node_hardware(self)

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        msg = msg.split('-')
        # id of the sender
        id = msg[0]
        if msg[1] == "decohered":
            # notify the link layer
            msg2 = packLinkExpired() #specify which link expired#
            self.send_message(self.parent_repeater, msg2)

    def swap_entanglement(self): 
        # proper quantum gates will be performed here.
        # find the positions of the qubits in the globalState state
        # apply the right qutip gates. Assume ideal gates at this point while you're
        # building the thing.
        # Do stuff to the global state container's state.
        CNOT = cnot(N=int(math.log2(self.global_state.state.shape[0])), control=self.left_qubit.id, target=self.right_qubit.id)
        new_state = CNOT * self.global_state.state * CNOT.dag()
        Z180 = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.left_qubit.id)
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=self.left_qubit.id)
        H = Y90 * Z180
        new_state = H * new_state * H.dag()
        self.global_state.update_state(new_state)
        measurement_result1 = self.measure(self.left_qubit[0])
        measurement_result2 = self.measure(self.right_qubit[0])     
        # notify the parent repeater so that it can send the classical data to
        # the other repeater.
        msg = {'msg' : "entanglement swapping done", 
               'measurement_result1' : measurement_result1,
               'measurement_result2' : measurement_result2}
        self.send_message(self.parent_repeater, msg)
        # Now the parent repeater should notify the remote repeater
        # that swapping is done and should give it the measurement results.

    def apply_swap_corrections(self, qubitId, measurement_result1, measurement_result2):
        if measurement_result1 == 0 and measurement_result1 == 0:
            return
        elif measurement_result1 == 0 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubitId)
        elif measurement_result1 == 1 and measurement_result1 == 0:
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubitId)
        elif measurement_result1 == 1 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubitId)
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubitId) * correction
        new_state = correction * self.global_state.state * correction.dag()
        self.global_state.update_state(new_state)
        msg = {'msg' : "entanglement swapping corrections applied"}
        self.send_message(self.parent_repeater, msg)

    def measure(self, qubit, axis = "01"):
        # https://inst.eecs.berkeley.edu/~cs191/fa14/lectures/lecture10.pdf
        print("measuring qubit in repeater hardware")
        rho = self.global_state.state
        # construct the projectors
        P0 = tensor([identity(2) for _ in range(qubit.id)] + 
                    basis(2,0) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.id + 1, int(math.log2(self.global_state.state.shape[0])))])
        P1 = tensor([identity(2) for _ in range(qubit.id)] + 
                    basis(2,1) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.id + 1, int(math.log2(self.global_state.state.shape[0])))])
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
        print("loading data from local qubit onto photon")
        # swaps the state of the photon and the local qubit 
        # (the photon should be initialized to |0>. The initialization 
        # can be noisy).
        SWAP = swap(N=int(math.log2(self.global_state.state.shape[0])), targets=[qubit.id, photon.id])
        newState = SWAP * self.global_state.state * SWAP.dag()
        self.global_state.update_state(newState)

    def unload_qubit_from_photon(self, qubit, photon):
        print("unloading data from photon onto local qubit")
        # swaps the state of the photon and the local qubit 
        # (the local qubit should be initialized to |0>. The initialization 
        # can be noisy). 
        SWAP = swap(N=int(math.log2(self.global_state.state.shape[0])), targets=[qubit.id, photon.id])
        new_state = SWAP * self.global_state.state * SWAP.dag()
        self.global_state.update_state(new_state)
        # notify the layers above that a qubit was received.
        fiber = self.left_fiber if qubit == self.left_qubit else self.right_fiber
        if photon.header == "link":
            msg = {'msg' : "received link qubit",  # this is the standard. Document it somewhere.
                   'sender' : fiber.node2 if self == fiber.node1 else fiber.node1,
                   'receiver' : self}
        else:
            msg = {'msg' : "received qubit",  # this is the standard. Document it somewhere.
                   'sender' : fiber.node2 if self == fiber.node1 else fiber.node1, 
                   'receiver' : self}
        if self.parent_repeater:
            self.send_message(self.parent_repeater, msg)
        photon.destroy()

    def send_photon_through_fiber(self, photon, fiber):
        fiber.carry_photon(photon, self)

    def receive_photon_from_fiber(self, photon, fiber):
        print("repeater hardware receiving photon")
        # This function is called by an optical fiber to
        # alert the repeaterHardware to receive the incoming photon.
        # The repeaterHardware chooses a (physical) qubit on which to unload the 
        # qubit carried on the photon.
        qubit = self.left_qubit if fiber == self.left_fiber else self.right_qubit
        self.unload_qubit_from_photon(qubit, photon)

    def attempt_link_creation(self, remote_node):
        # remote is a repeater object.
        # here the physical details of link creation will be implemented:
        # 1. create EPR pair on one of the local qubits and a photon.
        # 2. send the photon to the remote receiver.
        if self.left_fiber is None:
            fiber = self.right_fiber
        elif self.right_fiber is None:
            fiber = self.left_fiber
        elif self.left_fiber.is_connected(remote_node):
            fiber = self.left_fiber
        else:
            fiber = self.right_fiber
#         fiber = self.left_fiber if self.left_fiber.is_connected(remote_node) else self.right_fiber
        qubit = self.left_qubit if fiber == self.left_fiber else self.right_qubit
        qubit.reset()
        photon = Photon()
        photon.header = "link"
        Z180 = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubit.id)
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=qubit.id)
        H = Y90 * Z180
        new_state = H * self.global_state.state * H.dag()
        CNOT = cnot(N=int(math.log2(self.global_state.state.shape[0])), control=qubit.id, target=photon.id)
        new_state = CNOT * new_state * CNOT.dag()
        self.global_state.update_state(new_state)
        self.send_photon_through_fiber(photon, fiber)
        # notify parent_repeater
        if self.parent_repeater:
            msg = {'msg' : "sent link qubit",  # this is the standard. Document it somewhere.
                   'sender' : self, 
                   'receiver' : fiber.node2 if self == fiber.node1 else fiber.node1}
            self.parent_repeater.send_message(msg)
        # 3. (for later) check somehow that we have a good link.
        # support for heralding stations and photon transmission, etc.

    def attempt_distillation(self):
        # apply gates on the qubits here
        return
