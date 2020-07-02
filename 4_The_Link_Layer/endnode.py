%load_ext autoreload
%autoreload 2

from ../5_The_Physical_Layer import endnodeHardware

class endNode(object):
    def __init__(self):
        self.netId = None
        self.endnodeHardware = endnodeHardware(self)
        self.link = None
        self.cable = None

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

    def handleLinkCreationSuccess(self, other):
        self.links = other

    def handleLinkRequest(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attemptLinkCreation(#specify nodes here#)

    def requestLink(self, other):
        msg = packLinkRequest(self.netId)
        self.sendMessage(other, msg)
