%load_ext autoreload
%autoreload 2

import random
from qutip import *

from ./ import qubit

class endnodeHardware(object):
    def __init__(self, parentEndnode, globalState, opticalFiber, noOfQubits=1):
#         self.id = None
        self.parentEndnode = parentEndnode
        global globalState
        self.globalState = globalState
        self.qubit = qubit(self)
        self.opticalFiber = opticalFibers                                          
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
        theQubit = self.leftQubit if self.parentEndnode.id > remote.id else self.rightQubit
        theOpticalFiber = self.leftOpticalFiber if self.parentEndnode.id > remote.id else self.rightOpticalFiber
        thePhoton = theOpticalFiber.photon12 if self.id > remote.id else theOpticalFiber.photon12
        self.loadQubitOnPhoton(theQubit, thePhoton)
        self.sendPhoton(thePhoton, theOpticalFiber)
        # 3. (for later) check somehow that we have a good link.
        # support for heralding stations and photon transmission, etc.

    def attemptDistillation(self):
        # apply gates on the qubits here
        return
