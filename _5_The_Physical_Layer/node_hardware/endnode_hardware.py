import sys
import math
import random
from qutip import *

sys.path.append("../..")
from _5_The_Physical_Layer.qubit_carriers.qubit import Qubit
from _5_The_Physical_Layer.qubit_carriers.photon import Photon

from common.global_state_container import global_state_container

class EndnodeHardware(object):
    def __init__(self, parent_endnode, qubits=1):
        print("creating endnode hardware")
#         self.id = None
        self.parent_endnode = parent_endnode
        self.global_state = global_state_container.state
        self.upper_qubit = Qubit(self) # this qubit is used to support entanglement
        self.lower_qubit = Qubit(self) # this qubit is used to support entanglement
        self.memory_qubit = Qubit(self) # this qubit is used to store qubits that a user needs to send
        self.upper_fiber = None
        self.lower_fiber = None
#         self.memoryQubits = []

    def connect_fiber(self, fiber, upper_or_lower="lower"):
        print("connecting " + upper_or_lower + " fiber in endnode hardware")
        if upper_or_lower == "upper":
            self.upper_fiber = fiber
        else:
            self.lower_fiber = fiber
        fiber.connect_node_hardware(self)

    def teleport_qubit(self): # this does the same thing as repeater.hardware.entanglement_swap.
        print("teleporting qubit in endnode hardware.")
        CNOT = cnot(N=int(math.log2(self.global_state.state.shape[0])), control=self.memory_qubit.id, target=self.lower_qubit.id)
        new_state = CNOT * self.global_state.state * CNOT.dag()
        Z180 = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        H = Y90 * Z180
        new_state = H * new_state * H.dag()
        self.global_state.update_state(new_state)
        measurement_result1 = self.measure(self.memory_qubit)
        measurement_result2 = self.measure(self.lower_qubit) # we only use the upper qubit for distillation
        # notify the parent repeater so that it can send the classical data to
        # the other repeater.
        msg = {'msg' : "child hardware: Teleport done. Handle corrections.",
               'measurement_result1' : measurement_result1,
               'measurement_result2' : measurement_result2}
        self.send_message(self.parent_endnode, msg)

    def apply_teleport_corrections(self, measurement_result1, measurement_result2):
        print("applying teleport corrections in endnode hardware.")
        if measurement_result1 == 0 and measurement_result1 == 0:
            correction = None
        elif measurement_result1 == 0 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
        elif measurement_result1 == 1 and measurement_result1 == 0:
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
        elif measurement_result1 == 1 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id) * correction
        if correction:
            new_state = correction * self.global_state.state * correction.dag()
            self.global_state.update_state(new_state)
        msg = {'msg' : "child hardware: Teleport corrections applied."}
        self.send_message(self.parent_endnode, msg)

    def measure(self, qubit, axis = "01"):
        print("measuring qubit in endnode hardware")
        # https://inst.eecs.berkeley.edu/~cs191/fa14/lectures/lecture10.pdf
        rho = self.global_state.state
        # construct the projectors
        P0 = tensor([identity(2) for _ in range(qubit.id)] + 
                    [basis(2,0) * basis(2,0).dag()] + 
                    [identity(2) for _ in range(qubit.id + 1, int(math.log2(self.global_state.state.shape[0])))])
        P1 = tensor([identity(2) for _ in range(qubit.id)] + 
                    [basis(2,1) * basis(2,1).dag()] + 
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
        qubit = self.lower_qubit if fiber == self.lower_fiber else self.upper_qubit
        self.unload_qubit_from_photon(qubit, photon) # confusing names.
        
    def unload_qubit_from_photon(self, qubit, photon):
        print("unloading data from photon onto local qubit")
        # swaps the state of the photon and the local qubit 
        # (the local qubit should be initialized to |0>. The initialization 
        # can be noisy). 
        SWAP = swap(N=int(math.log2(self.global_state.state.shape[0])), targets=[qubit.id, photon.id])
        new_state = SWAP * self.global_state.state * SWAP.dag()
        self.global_state.update_state(new_state)
        # notify the layers above that a qubit was received.
        upper_or_lower = "upper" if qubit == self.upper_qubit else "lower"
        fiber = self.upper_fiber if upper_or_lower == "upper" else self.lower_fiber
        sender = fiber.node2 if self == fiber.node1 else fiber.node1
        if photon.header == "link":
            print("received link qubit in endnode hardware")
            msg = {'msg' : "child hardware: Received link qubit.",  # this is the standard. Document it somewhere.
                   'sender' : sender, 
                   'receiver' : self,
                   'upper_or_lower' : upper_or_lower,
                   'link' : photon.link}
        else:
            msg = {'msg' : "child hardware: Received qubit.",  # this is the standard. Document it somewhere.
                   'sender' : sender, 
                   'receiver' : self,
                   'upper_or_lower' : upper_or_lower}
        photon.destroy()
        if self.parent_endnode:
            self.send_message(self.parent_endnode, msg)

    def attempt_link_creation(self, remote_hardware, upper_or_lower="lower"):
        print("attempting link creation in endnode hardware.")
        # remote is a repeater object.
        # here the physical details of link creation will be implemented:
        # 1. create EPR pair. Store one half locally and load the other on a photon.
        # 2. send the photon to the remote receiver.
        fiber = self.upper_fiber if upper_or_lower == "upper" else self.lower_fiber
        qubit = self.upper_qubit if upper_or_lower == "upper" else self.lower_qubit
        link = None # this is a link layer object so it might be silly to use it like this.
        if self.parent_endnode:
            if upper_or_lower == "upper":
                link = self.parent_endnode.upper_link
            else:
                link = self.parent_endnode.lower_link
        qubit.reset()
        photon = Photon()
        photon.header = "link"
        photon.link = link
        Z180 = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=qubit.id)
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=qubit.id)
        H = Y90 * Z180
        new_state = H * self.global_state.state * H.dag()
        CNOT = cnot(N=int(math.log2(self.global_state.state.shape[0])), control=qubit.id, target=photon.id)
        new_state = CNOT * new_state * CNOT.dag()
        self.global_state.update_state(new_state)
        self.send_photon_through_fiber(photon, fiber)
        # notify parent_repeater
        if self.parent_endnode:
            msg = {'msg' : "child hardware: Sent link qubit.",  # this is the standard. Document it somewhere.
                   'sender' : self, 
                   'receiver' : fiber.node2 if self == fiber.node1 else fiber.node1,
                   'upper_or_lower' : upper_or_lower}
            self.send_message(self.parent_endnode, msg)
        # 3. (for later) check somehow that we have a good link.
        # support for heralding stations and photon transmission, etc.

    def attempt_distillation(self):
        # apply gates on the qubits here
        return

    def apply_swap_corrections(self, measurement_result1, measurement_result2):
        print("applying swap corrections in endnode hardware")
        if measurement_result1 == 0 and measurement_result1 == 0:
            correction = None
        elif measurement_result1 == 0 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
        elif measurement_result1 == 1 and measurement_result1 == 0:
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
        elif measurement_result1 == 1 and measurement_result1 == 1:
            correction = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id)
            correction = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.lower_qubit.id) * correction
        if correction:
            new_state = correction * self.global_state.state * correction.dag()
            self.global_state.update_state(new_state)
        msg = {'msg' : "child hardware: Entanglement swapping corrections applied."}
        self.send_message(self.parent_endnode, msg)

    def load_zero_on_memory_qubit(self):
        print("loading |0> state on memory qubit in endnode hardware")
        return # we don't need to do anything because the qubit is initialize in this state

    def load_one_on_memory_qubit(self):
        print("loading |1> state on memory qubit in endnode hardware")
        X180 = rx(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        new_state = X180 * self.global_state.state * X180.dag()
        self.global_state.update_state(new_state)

    def load_plus_on_memory_qubit(self):
        print("loading |+> state on memory qubit in endnode hardware")
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        new_state = Y90 * self.global_state.state * Y90.dag()
        self.global_state.update_state(new_state)

    def load_minus_on_memory_qubit(self):
        print("loading |-> state on memory qubit in endnode hardware")
        Y90  = ry(90, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        Z180 = rz(180, N=int(math.log2(self.global_state.state.shape[0])), target=self.memory_qubit.id)
        G = Z189 * Y90
        new_state = G * self.global_state.state * G.dag()
        self.global_state.update_state(new_state)

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        return
