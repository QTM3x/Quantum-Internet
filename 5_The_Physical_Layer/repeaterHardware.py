%load_ext autoreload
%autoreload 2

import random
from qutip import *

from ./ import qubit

class repeaterHardware(object):
    def __init__(self, parentRepeater, globalState, opticalFibers, noOfQubits=2):
        self.parentRepeater = parentRepeater
        global globalState
        self.globalState = globalState
        self.leftQubit = qubit(self)
        self.rightQubit = qubit(self)
        self.leftOpticalFiber = opticalFibers[0]
        self.rightOpticalFiber = opticalFibers[1]                                          
#         self.memoryQubits = []

    def sendMessage(self, obj, msg):
        obj.handleMessage(msg)

    def handleMessage(self, msg):
        msg = msg.split('-')
        # id of the sender
        id = msg[0]
        if msg[1] === "decohered":
            # notify the link layer
            msg2 = packLinkExpired(#specify which link expired#)
            self.sendMessage(self.parentRepeater, msg2)

    def swapEntanglement(self): 
        # proper quantum gates will be performed here.
        # find the positions of the qubits in the globalState state
        # apply the right qutip gates. Assume ideal gates at this point while you're
        # building the thing.
        # Do stuff to the global state container's state.
        CNOT = cnot(N=globalState.N, control=self.leftQubit[0].id, target=self.rightQubit[0].id)
        newState = CNOT * self.globalState.state * CNOT.dag()
        Z180 = rz(180, N=self.globalState.N, target=self.leftQubit[0].id)
        Y90  = ry(90, N=self.globalState.N, target=self.leftQubit[0].id)
        H = Y90 * Z180
        newState = H * newState * H.dag()
        self.globalState.updateState(newState)
        measurement_result1 = self.measure(self.leftQubit[0])
        measurement_result2 = self.measure(self.rightQubit[0])     
        # notify the parent repeater so that it can send the classical data to
        # the other repeater.
        msg = {'msg' : "entanglement swapping done", 
               'measurement_result1' : measurement_result1,
               'measurement_result2' : measurement_result2}
        self.sendMessage(self.parentRepeater, msg)
        # Now the parent repeater should notify the remote repeater
        # that swapping is done and should give it the measurement results.

    def applySwapCorrections(self, qubitId, measurement_result1, measurement_result2):
        if measurement_result1 == 0 and measurement_result1 == 0:
            return
        elif measurement_result1 == 0 and measurement_result1 == 1:
            correction = rz(180, N=self.globalState.N, target=qubitId)
        elif measurement_result1 == 1 and measurement_result1 == 0:
            correction = rx(180, N=self.globalState.N, target=qubitId)
        elif measurement_result1 == 1 and measurement_result1 == 1:
            correction = rz(180, N=self.globalState.N, target=qubitId)
            correction = rx(180, N=self.globalState.N, target=qubitId) * correction
        newState = correction * self.globalState.state * correction.dag()
        self.globalState.updateState(newState)
        msg = {'msg' : "entanglement swapping corrections applied"}
        self.sendMessage(self.parentRepeater, msg)

    def measure(self, qubit, basis = "01"):
        # https://inst.eecs.berkeley.edu/~cs191/fa14/lectures/lecture10.pdf
        rho = self.globalState.state
        # construct the projectors
        P0 = tensor([identity(2) for _ in range(qubit.Id)] + 
                    basis(2,0) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.Id + 1, self.globalState.N)])
        P1 = tensor([identity(2) for _ in range(qubit.Id)] + 
                    basis(2,1) * basis(2,0).dag() + 
                    [identity(2) for _ in range(qubit.Id + 1, self.globalState.N)])
        # compute the probabilities of the 1 and 0 outcomes
        p0 = (P0 * rho).tr()
        p1 = (P1 * rho).tr() # check that p1 = 1 - p0
        # choose an outcome at random using the probabilities above.
        result = 0 if random.random() < p0 else 1
        # simulate state collapse
        newState = P0 * rho * P0 / p0 if result == 0 else P1 * rho * P1 / p1
        # update globalState
        self.globalState.updateState(newState)
        # return the measurement result
        return result

    def loadQubitOnPhoton(self, qubit, photon):  # both qubit and photon are qubit objects
        # swaps the state of the photon and the local qubit 
        # (the photon should be initialized to |0>. The initialization 
        # can be noisy).
        SWAP = swap(N=self.globalState.N, targets=[qubit.id, photon.id])
        newState = SWAP * self.globalState.state * SWAP.dag()
        self.globalState.updateState(newState)

    def unloadQubitFromPhoton(self, qubit, photon):
        # swaps the state of the photon and the local qubit 
        # (the local qubit should be initialized to |0>. The initialization 
        # can be noisy). 
        SWAP = swap(N=self.globalState.N, targets=[qubit.id, photon.id])
        newState = SWAP * self.globalState.state * SWAP.dag()
        self.globalState.updateState(newState)

    def sendPhoton(self, photon, opticalFiber):
        opticalFiber.carryPhoton(photon)

    def receivePhoton(self, photon):
        # This function is called by an optical fiber to
        # alert the repeaterHardware to receive the incoming photon.
        # The repeaterHardware chooses a (physical) qubit on which to unload the 
        # qubit carried on the photon.
        self.unloadQubitFromPhoton(qubit, photon)

    def attemptLinkCreation(self, remote):
        # remote is a repeater object.
        # here the physical details of link creation will be implemented:
        # 1. create EPR pair. Store one half locally and load the other on a photon.
        # 2. send the photon to the remote receiver.
        theQubit = self.leftQubit if self.parentRepeater.netId > remote.netId else self.rightQubit
        theOpticalFiber = self.leftOpticalFiber if self.parentRepeater.netId > remote.netId else self.rightOpticalFiber
        thePhoton = theOpticalFiber.photon12 if self.parentRepeater.netId > remote.netId else theOpticalFiber.photon12
        self.loadQubitOnPhoton(theQubit, thePhoton)
        self.sendPhoton(thePhoton, theOpticalFiber)
        # 3. (for later) check somehow that we have a good link.
        # support for heralding stations and photon transmission, etc.

    def attemptDistillation(self):
        # apply gates on the qubits here
        return
