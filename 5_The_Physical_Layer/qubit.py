%load_ext autoreload
%autoreload 2

class qubit(object):
    def __init__(id, state, decoherenceTime, parentRepeaterHardware):
        self.id = id
        self.state = state
        self.decoherenceTime = decoherenceTime
        self.parentRepeaterHardware = parentRepeaterHardware
    
    # move these sendMessage functions to an external function
    # This function is a wire running from the qubit to the repeater hardware.
    # Can we detect when a qubit has decohered?
    def sendMessage(self, obj, msg):
        obj.handleMessage(msg)
        
    def decohere():
        msg = packQubitDecohered(self.id)
        self.sendMessage(self.parentRepeaterHardware, msg)
