
import sys

from qutip import *
import math

sys.path.append("..")
from common.gui import gui
print("imported gui", gui)

# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
def init():
    global state
    state = GlobalState()
    

class GlobalState(object):
    def __init__(self):
#         self.N = N # the number of qubits
#         GUI.init()
#         self.M = N - 1 # this is the number of optical fibers
        self.state = None # everything starts in the |000..0> state.
        
    def update_state(self, newState):
        self.state = newState
        # UpdateGUI here and only here.
        # Use the GUI as a global object
#         if GUI.GUI is not None:
#             GUI.GUI.update_gui()
        try:
            gui.update_gui()
        except:
            print("GUI not on")
            
    # schedule quantum gates and maps to make 
    # it like a circuit with everything in the right order.
    # Do it with a queue like the GUI.
  
    def apply_channel(self, channel, qubitId):
        # act with the channel on the appropritate qubit.
        # qutip knows how to do this.
        pass

    # returns the fidelity of the link between any two qubits in the network.
    def get_fidelity(self, qubit1, qubit2):
        pass
    
    def create_qubit(self):
        if self.state is None:
            new_state = basis(2,0) * basis(2,0).dag()
        else:
            new_state = tensor(self.state, basis(2,0) * basis(2,0).dag())
        self.update_state(new_state)
        number_of_qubits = int(math.log2(self.state.shape[0]))
        return number_of_qubits
