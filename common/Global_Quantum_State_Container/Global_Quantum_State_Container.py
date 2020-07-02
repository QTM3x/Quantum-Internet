
from qutip import *

class globalState(object):
    def __init__(self, N):
        self.N = N # the number of qubits
        self.M = N - 1 # this is the number of optical fibers
        self.state = basis(2**(N + 2*self.M), 0) # everything starts in the |000..0> state.
        
    def updateState(self, newState):
        self.state = newState
        # UpdateGUI here and only here.
        # Use the GUI as a global object
        if !!GUI:
            GUI.updateGUI()
            
    # schedule quantum gates and maps to make 
    # it like a circuit with everything in the right order.
    # Do it with a queue like the GUI.
  
    def applyChannel(self, channel, qubitId):
        # act with the channel on the appropritate qubit.
        # qutip knows how to do this.

    # returns the fidelity of the link between any two qubits in the network.
    def fidelity(self, qubit1, qubit2):
        pass
    
    def newQubit(self):
        newState = tensor(basis(2,0) * basis(2,0).dag(), self.state)
        self.updateState(newState)
    
    def getNumberOfQubits(self):
        pass
