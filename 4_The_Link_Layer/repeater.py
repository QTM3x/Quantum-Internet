%load_ext autoreload
%autoreload 2

from ../5_The_Physical_Layer import repeaterHardware

class repeater(object):
    def __init__(self, parentRepeaterChain, noOfLinks=1):
        self.netId = None
        self.parentRepeaterChain = parentRepeaterChain
        self.repeaterHardware = repeaterHardware(self)
        self.leftLink = None
        self.rightLink = None
        self.leftCable = None
        self.rightCable = None

    def attemptSwap(self, leftLink, rightLink):
        self.repeaterHardware.swapEntanglement()
        # wait for repeaterHardware to tell us when/if the swap is done.

    # attempt to create link with another repeater
    def attemptLinkCreation(self, other):
        # attempt link creation on the next free qubit
        self.repeaterHardware.attemptLinkCreation(other)

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
#         msg = msg.split('-')
#         # id of the sender
#         id = msg[0]
            
#         if msg[1] === "swap": 
#             if msg[2] === "success":
#                 self.handleSwapSuccess()     
#         elif msg[1] === "link":
#             if   msg[2] === "request":
#                 self.handleLinkRequest()
#             elif msg[2] === "deny":
#                 self.handleLinkDeny()
#             elif msg[2] === "success":
#                 fidelity = float(msg[3])
#                 self.handleLinkCreationSuccess()
#             elif msg[2] === "expired":
#                 if link is not None:
#                     # notify the repeater on the other side of the link
#                     # so that it also frees up resources.
#                     msg2 = packLinkExpired(self.id)
#                     self.sendMessage()
#                     # reset link to None.
                    
        # use dictionaries for messages
        
        if msg['msg'] == "entanglement swapping done":
            # update connections table
            self.handleSwapSuccess(..., ...)
            # retitle the message and forward it.
            # Note that the msg contains two measurement results.
            msg['msg'] = "entanglement swapping corrections"
            self.sendMessage(remoteRepeater, msg)
        elif msg['msg'] == "entanglement swapping corrections":
            measurement_result1 = msg['measurement_result1']
            measurement_result2 = msg['measurement_result2']
            # assume we have received the qubit already.
            # ask the repeaterHardware to apply corrections.
            self.repeaterHardware.applySwapCorrections(qubitId,
                                                       measurement_result1, 
                                                       measurement_result2)
        elif msg['msg'] == "entanglement swapping corrections applied":
            # update connections table
            self.handleSwapSuccess(..., ...)
        else:
            print("received unknown message")

    def handleSwapSuccess(self, leftLinkIndex, rightLinkIndex):
        # reset swapped links
        self.leftLinks[leftLinkIndex] = None
        self.rightLinks[rightLinkIndex] = None
        #notify parent repeater chain (network layer)
        msg = packSwapSuccess(...)
        self.sendMessage(self.parentRepeaterChain, msg)

    def handleLinkCreationSuccess(self, side, other):
        if side === "left":
            self.leftLink = other
        elif side === "right":
            self.rightLink = other
    
    def handleLinkRequest(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attemptLinkCreation(#specify nodes here#)

    def requestLink(self, other):
        msg = packLinkRequest(self.netId)
        self.sendMessage(other, msg)
