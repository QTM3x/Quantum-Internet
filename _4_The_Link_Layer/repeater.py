import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.repeater_hardware import RepeaterHardware
print("imported RepeaterHardware object", RepeaterHardware)
from link import Link
print("imported Link object", Link)

class Repeater(object):
    def __init__(self, parent_repeater_chain, n=1):
        print("creating new repeater")
        self.netId = None
        self.parent_repeater_chain = parent_repeater_chain
        self.hardware = RepeaterHardware(self)
        self.left_link = None
        self.right_link = None
        self.left_cable = None
        self.right_cable = None

    def connect_right_cable(self, cable):
        print("connecting right cable in repeater")
        self.right_cable = cable
        self.hardware.connect_right_fiber(cable.optical_fiber)
        cable.connect_node(self)
        
    def connect_left_cable(self, cable):
        print("connecting left cable in repeater")
        self.left_cable = cable
        self.hardware.connect_left_fiber(cable.optical_fiber)
        cable.connect_node(self)
    
    def attemptSwap(self, left_link, right_link):
        self.hardware.swap_entanglement()
        # wait for repeaterHardware to tell us when/if the swap is done.

    # attempt to create link with another repeater
    def attempt_link_creation(self, node):
        # attempt link creation on the next free qubit
        self.hardware.attempt_link_creation(node.hardware)

    # attempt to do entanglement distillation of 
    # two links with the same repeater.
    def attempt_distillation(self, links):
        self.hardware.attempt_distillation()

    # this function emits a signal to the link layer (which here takes the form 
    # of software running on the repeater).
    def send_message(self, obj, msg):
        obj.handle_message(msg)

    # this function receives an emitted signal
    def handle_message(self, msg):
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
            self.hardware.apply_swap_corrections(qubitId,
                                                       measurement_result1, 
                                                       measurement_result2)
        elif msg['msg'] == "entanglement swapping corrections applied":
            # update connections table
#             self.handle_swap_success(..., ...)
            return
        elif msg['msg'] == "received qubit":
            return
        elif msg['msg'] == "received link qubit":
            sender = msg['sender'].parent_repeater # sender is a node hardware
            side = "left" if sender in (self.left_cable.node1, self.left_cable.node2) else "right"
            if side == "left":
                self.left_link = sender.right_link
                self.left_link.node2 = self
            else:
                self.right_link = sender.left_link
                self.right_link.node2 = self
            # notify the parent repeater chain
            if self.parent_repeater_chain:
                msg = {'msg' : "link created",
                       'link': self.left_link if side == "left" else self.right_link,
                       'side': side}
                self.send_message(self.parent_repeater_chain)
        elif msg['msg'] == "sent link qubit":
            receiver = msg['receiver'].parent_repeater # change this to parent node throughout
            side = "left" if receiver in (self.left_cable.node1, self.left_cable.node2) else "right"
            if side == "left":
                self.left_link = Link()
                self.left_link.node1 = self
            else:
                self.right_link = Link()
                self.right_link.node1 = self
        else:
            print("received unknown message")

    def handle_swap_success(self):
        # reset swapped links
        self.left_link = None
        self.right_link = None
        #notify parent repeater chain (network layer)
        msg = packSwapSuccess(...)
        self.send_message(self.parent_repeater_chain, msg)

#     def handle_link_creation_success(self, side, remote_repeater):
#         if side == "left":
#             self.left_link = remote_repeater
#         elif side == "right":
#             self.right_link = remote_repeater
    
    def handle_link_request(self):
        # determine if the other repeater is on the left or right
            
        # check if there is a node available on that side 
            
        if slotAvailable:
            # create the link
            self.attempt_link_creation() #specify nodes here#

    def request_link(self, remote_repeater):
        msg = pack_link_request(self.netId)
        self.send_message(other, msg)
