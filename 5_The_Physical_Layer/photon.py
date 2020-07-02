%load_ext autoreload
%autoreload 2

class photon(object):
    def __init__(self, parentOpticalFiber):
        global globalState
        self.globalState = globalState
        self.id = self.globalState.newQubit()
        self.parentOpticalFiber = parentOpticalFiber
        
    # reset the state of the photon to the pure |0> state. 
    # This should be done everytime the qubit is used, 
    # because in real experiments the photon is absorbed 
    # and we have to use a new photon.
    def reset(self):               
        # Resetting is non-trivial! If the qubit 
        # you are initialization /reseting is entangled with other 
        # qubits you can mess up, or more precisely, lose track, of 
        # the state of the other qubits. The other qubit becomes 
        # entangled with the environment, which we generally 
        # don't have access to.
        pass 
