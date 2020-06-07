%load_ext autoreload
%autoreload 2

from ../5_The_Physical_Layer import repeaterHardware

class repeater(object):
    def __init__(id = "0", parentRepeaterChain, noOfLinks = 1):
        self.id = id
        self.parentRepeaterChain = parentRepeaterChain
        self.repeaterHardware = new repeaterHardware(noOfLinks, self)
        # list of links to the right and left.
        self.rightLinks = [None for _ in range(noOfLinks)]
        self.leftLinks = [None  for _ in range(noOfLinks)]
        
        
    def attemptSwap(self, leftLink, rightLink):
        self.repeaterHardware.attemptSwap(#corrsponding qubits#)
        # wait for repeaterHardware to tell us when/if the swap is done.
            
    # attempt to create link with another repeater
    def attemptLinkCreation(self, other):
        # attempt link creation on the next free qubit
        self.repeaterHardware.attemptLinkCreation()
            
    # attempt to do entanglement distillation of 
    # two links with the same repeater.
    def attemptDistillation(self, other, links):
        self.repeaterHardware.attemptDistillation()
            
    # this function emits a signal to the link layer (which here takes the form 
    # of software running on the repeater).
    def sendMessage(self, obj, msg):
        obj.handleMessage(msg)
            
    # this function receives an emitted signal
    def handleMessage(self, msg):
        #handle message#
        msg = msg.split('-')
        # id of the sender
        id = msg[0]
            
        if msg[1] === "swap": 
            if msg[2] === "success":
                self.handleSwapSuccess()     
        elif msg[1] === "link":
            if   msg[2] === "request":
                self.handleLinkRequest()
            elif msg[2] === "deny":
                self.handleLinkDeny()
            elif msg[2] === "success":
                fidelity = float(msg[3])
                self.handleLinkCreationSuccess()
            elif msg[2] === "expired":
                if link is not None:
                    # notify the repeater on the other side of the link
                    # so that it also frees up resources.
                    msg2 = packLinkExpired(self.id)
                    self.sendMessage()
                    # reset link to None.
                
            
            
    def handleSwapSuccess(self, leftLinkIndex, rightLinkIndex):
        # reset swapped links
        self.leftLinks[leftLinkIndex] = None
        self.rightLinks[rightLinkIndex] = None
        #notify parent repeater chain (network layer)
        msg = packSwapSuccess(...)
        self.sendMessage(self.parentRepeaterChain, msg)
            
    def handleLinkCreationSuccess(self, side, linkIndex, other):
        if side === "left":
            self.leftLinks[linkIndex] = other
        elif side === "right":
            self.rightLinks[linkIndex] = other
                
    def handleLinkRequest(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attemptLinkCreation(#specify nodes here#)
    
    def requestLink(self, other):
        msg = packLinkRequest(self.id)
        self.sendMessage(other, msg)
  
