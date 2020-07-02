%load_ext autoreload
%autoreload 2

class qubit(object):
    def __init__(self, decoherenceTime, parentHardware):
        global globalState
        self.globalState = globalState
        self.id = self.globalState.newQubit()
        self.decoherenceTime = decoherenceTime
        self.parentHardware = parentHardware
        
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
        gate = tensor([identity(2) for _ in range(globalState.N)])
        newState = gate * self.globalState.state * gate.dag()  # for now the map is a identity unitary gate
        self.globalState.updateState(newState)

#     while True:
#         # gradually decohere. Do it in a thread.
        # see whiteboard for the new way
