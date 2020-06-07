%load_ext autoreload
%autoreload 2

class application(object): # this code runs on the user's PQC (personal quantum computer)
    def __init__(quantumInternet, locationOnNetwork):
        self.quantumInternet = quantumInternet
        # localNode is the device the application is running on
        self.localNode = self.quantumInternet.repeaterChain.repeaters[locationOnNetwork] 
        # for now locationOnNetwork can be 0 or len(self.quantumInternet.repeaterChain.repeaters) - 1 
        pass

    def teleportQubit(qubit, receiverId):
        # check if we have a link with receiverId
        
        # if we don't have one, request one
        self.quantumIntenet.requestLink("Bob")
        # send the classical bits to Bob
        qInternet.text("Bob", "bits are " + ...)
