%load_ext autoreload
%autoreload 2

from ./ import qubit

class repeaterHardware(object):
    def __init__(noOfQubits, parentRepeater):
        self.parentRepeater = parentRepeater
        # the order of the qubits in these lists is the same as the order
        # of the links in the link lists in the repeater class.
        self.rightQubits = [new qubit(1, self) for _ in range(noOfQubits)]
        self.leftQubits = [new qubit(1, self) for _ in range(noOfQubits)]
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

    def attemptSwap(self): # proper quantum gates will be performed here.
        
        # reset qubits
        
        # pack message with result
        # fidelity of the create link. (how do we compute this?)
        fidelity = ...
        msg = packSwapResult("success", fidelity) # should be of the form "swap-success-fidelity-0.5".
        # send message to parent repeater (link layer)
        self.sendMessage(self.parentRepeater, msg)
     
    def attemptLinkCreation(self): 
        # here the physical details of link creation will be implemented:
        # support for heralding stations and photon transmission, etc.
        if success:
            fidelity = ... 
            msg = packLinkCreationSuccess("success", fidelity)
            self.sendMessage(self.parentRepeater, msg)
        pass
                
    def attemptDistillation(self):
        # apply gates on the qubits here
        pass
    
