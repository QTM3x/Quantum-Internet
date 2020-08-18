
import sys

from qutip import *
import math

sys.path.append("../..")
from common.GUI import GUI
# print("imported gui", gui)

# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
def init():
    global state
    state = GlobalState()


class GlobalState(object):
    def __init__(self):
        GUI.init()
        self.state = None
#         self.id_count = 0
        self.qubit_carriers_list = []
        
    def update_state(self, new_state):
        self.state = new_state
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
    
    def create_qubit(self, qubit_carrier):
        print("creating new qubit in global state")
        # print("before:", self.state)
        if self.state is None:
            new_state = basis(2,0) * basis(2,0).dag()
        else:
            new_state = tensor(self.state, basis(2,0) * basis(2,0).dag())
        self.update_state(new_state)
        # print("after:", self.state)
        self.qubit_carriers_list.append(qubit_carrier)
#         self.id_count += 1
        # print(self.qubit_carriers_list)
        return len(self.qubit_carriers_list)-1
    
    def destroy_qubit(self, qubit_id):
        print("destroying qubit", qubit_id, "in global state")
        # print("before:", self.state)
        keep_systems = [i for i in range(len(self.qubit_carriers_list))]
        del keep_systems[qubit_id]
        self.update_state(self.state.ptrace(keep_systems)) #trace out the qubit
        del self.qubit_carriers_list[qubit_id]
        # print(self.qubit_carriers_list)
        self.update_ids()
        # print("after:", self.state)

    def get_qubit_state(self, qubit_id):
        return self.state.ptrace(qubit_id)
        
    def update_ids(self):
        for carrier in self.qubit_carriers_list:
            carrier.id = self.qubit_carriers_list.index(carrier)
