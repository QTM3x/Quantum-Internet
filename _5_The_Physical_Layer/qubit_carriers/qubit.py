
import sys

sys.path.append("../..")
from common.global_state_container import global_state_container

class Qubit(object):
    def __init__(self, parent_hardware, decoherence_time=1):
        print("creating new qubit")
        self.global_state = global_state_container.state
        self.id = self.global_state.create_qubit()
        self.decoherence_time = decoherence_time
        self.parent_hardware = parent_hardware
        
    # reset the state of the qubit to the pure |0> state.    
    def reset(self):               
        # Resetting is non-trivial! If the qubit 
        # you are initialization /reseting is entangled with other 
        # qubits you can mess up, or more precisely, lose track, of 
        # the state of the other qubits. The other qubit becomes 
        # entangled with the environment, which we generally 
        # don't have access to.
        pass 


#     def applyChannel(self, channel):
#         Global_Quantum_State_Container.applyChannel(channel)
        


    # move these sendMessage functions to an external function
    # This function is a wire running from the qubit to the repeater hardware.
    # Can we detect when a qubit has decohered?
#     def sendMessage(self, obj, msg):
#         obj.handleMessage(msg)
        
    def decohere(self): # decoherence should happen gradually. How can we do that?
#         channel = rx(phi, N=globalState.N, target=self.id):  # note that the id of the qubit is its position in the chain
        # apply decoherence map here
        gate = tensor([identity(2) for _ in range(self.global_state.N)])
        new_state = gate * self.global_state.state * gate.dag()  # for now the map is a identity unitary gate
        self.global_state.update_state(new_state)

#     while True:
#         # gradually decohere. Do it in a thread.
        # see whiteboard for the new way
