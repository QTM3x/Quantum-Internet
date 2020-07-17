import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.repeater_hardware import RepeaterHardware
print("imported RepeaterHardware object", RepeaterHardware)

class Repeater(object):
    def __init__(self, parent_repeater_chain, n=1):
        print("creating new repeater")
        self.netId = None
        self.parent_repeater_chain = parent_repeater_chain
        self.repeater_hardware = RepeaterHardware(self)
        self.left_link = None
        self.right_link = None
        self.left_cable = None
        self.right_cable = None

    def connect_right_cable(self, cable):
        print("connecting right cable in repeater")
        self.right_cable = cable
        self.repeater_hardware.connect_right_fiber(cable.optical_fiber)
        
    def connect_left_cable(self, cable):
        print("connecting left cable in repeater")
        self.left_cable = cable
        self.repeater_hardware.connect_left_fiber(cable.optical_fiber)
    
    def attemptSwap(self, left_link, right_link):
        self.repeater_hardware.swap_entanglement()
        # wait for repeaterHardware to tell us when/if the swap is done.

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
            self.handle_swap_success(..., ...)
            # retitle the message and forward it.
            # Note that the msg contains two measurement results.
            msg['msg'] = "entanglement swapping corrections"
            self.send_message(remote_repeater, msg)
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

    def handle_swap_success(self):
        # reset swapped links
        self.left_link = None
        self.right_link = None
        #notify parent repeater chain (network layer)
        msg = packSwapSuccess(...)
        self.send_message(self.parent_repeater_chain, msg)

    def handle_link_creation_success(self, side, remote_repeater):
        if side == "left":
            self.left_link = remote_repeater
        elif side == "right":
            self.right_link = remote_repeater
    
    def handle_link_request(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attempt_link_creation() #specify nodes here#

    def request_link(self, remote_repeater):
        msg = pack_link_request(self.netId)
        self.send_message(other, msg)
