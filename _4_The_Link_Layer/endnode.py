
from ../5_The_Physical_Layer import EndnodeHardware
print("imported EndnodeHardware object", EndnodeHardware)

class Endnode(object):
    def __init__(self):
        print("creating new endnode")
        self.netId = None
        self.endnode_hardware = EndnodeHardware(self)
        self.link = None
        self.cable = None

    # attempt to create link with another repeater
    def attempt_link_creation(self, remote_repeater):
        # attempt link creation on the next free qubit
        self.repeater_hardware.attempt_link_creation(remote_repeater)

    # attempt to do entanglement distillation of 
    # two links with the same repeater.
    def attempt_distillation(self, links):
        self.repeater_hardware.attempt_distillation()

    # this function emits a signal to the link layer (which here takes the form 
    # of software running on the repeater).
    def send_message(self, obj, msg):
        obj.handle_message(msg)

    # this function receives an emitted signal
    def handle_message(self, msg):
        if msg['msg'] == "entanglement swapping done":
            # update connections table
            self.handle_swapSuccess(..., ...)
            # retitle the message and forward it.
            # Note that the msg contains two measurement results.
            msg['msg'] = "entanglement swapping corrections"
            self.sendMessage(remote_epeater, msg)
        elif msg['msg'] == "entanglement swapping corrections":
            measurement_result1 = msg['measurement_result1']
            measurement_result2 = msg['measurement_result2']
            # assume we have received the qubit already.
            # ask the repeaterHardware to apply corrections.
            self.repeater_hardware.apply_swap_corrections(qubitId,
                                                       measurement_result1, 
                                                       measurement_result2)
        elif msg['msg'] == "entanglement swapping corrections applied":
            # update connections table
            self.handle_swap_success(..., ...)
        else:
            print("received unknown message")

    def handle_link_creation_success(self, other):
        self.links = other

    def handle_link_request(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attempt_link_creation(#specify nodes here#)

    def request_link(self, other):
        msg = packLinkRequest(self.netId)
        self.send_message(other, msg)
