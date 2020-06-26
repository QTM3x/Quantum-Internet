
from qutip import *

class globalState(object):
    def __init__(self, n):
        self.n = n # the number of qubits
        self.state = basis(2**n, 0)
        
    def updateState(self, newState):
        self.state = newState
        # updateGUI here and only here. Let it get the latest changes from the global state,
        # and not from the many components in the stack.
    
    # returns the fidelity of the link between any two qubits in the network.
    def fidelity(self, qubit1, qubit2):
        pass
