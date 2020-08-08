import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.endnode_hardware import EndnodeHardware
print("imported EndnodeHardware object", EndnodeHardware)

class Endnode(object):
    def __init__(self):
        print("creating new endnode")
        self.netId = None
        self.hardware = EndnodeHardware(self)
        self.link = None
        self.cable = None
        self.parent_application = None
        
    def connect_cable(self, cable):
        print("connecting cable in endnode")
        self.cable = cable
        self.hardware.connect_fiber(cable.optical_fiber)
        cable.connect_node(self)

    def teleport_qubit(self):
        self.hardware.teleport_qubit()

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
#         if msg['msg'] == "entanglement swapping done":
#             # update connections table
#             self.handle_swapSuccess(..., ...)
#             # retitle the message and forward it.
#             # Note that the msg contains two measurement results.
#             msg['msg'] = "entanglement swapping corrections"
#             self.sendMessage(remote_epeater, msg)
#         elif msg['msg'] == "entanglement swapping corrections":
#             measurement_result1 = msg['measurement_result1']
#             measurement_result2 = msg['measurement_result2']
#             # assume we have received the qubit already.
#             # ask the repeaterHardware to apply corrections.
#             self.hardware.apply_swap_corrections(qubitId,
#                                                        measurement_result1, 
#                                                        measurement_result2)
#         elif msg['msg'] == "entanglement swapping corrections applied":
#             # update connections table
#             self.handle_swap_success(..., ...)
#         else:
#             print("received unknown message")
        if msg['msg'] == "received qubit":
            if self.parent_application:
                self.parent_application.receive_qubit()
        elif msg['msg'] == "hardware: teleport done":
            # give the measurement results to the quantum internet, 
            # because I guess the quantum internet still has to do some
            # stuff.
            msg = {'msg' : "endnode: teleport done",
                   'measurement_result1' : msg['measurement_result1'],
                   'measurement_result2' : msg['measurement_result2'],
                   'sender_node' : self,
                   'receiver_node' : self.link.node1 if self == self.link.node2 else self.link.node2}
            self.send_message(
                self.parent_application.quantum_internet,
                msg
            )
        elif msg['msg'] == "endnode: teleport done":
            # a node is telling us that it has teleported us something, 
            # and is giving us the correction bits. So we'd better apply
            # these corrections.
            self.hardware.apply_teleport_corrections(msg['measurement_result1'], 
                                                       msg['measurement_result2'])
        elif msg['msg'] == "teleport corrections applied":
            # notify the parent application that it has received a qubit
            msg = {'msg' : "qubit received"}
            self.send_message(self.parent_application, msg)

    def handle_link_creation_success(self, other):
        self.link = other

#     def handle_link_request(self):
#         # determine if the other repeater is on the left or right
            
#         # check if there is a node available on that side 
            
#         if slotAvailable:
#             # create the link
#             self.attempt_link_creation() #specify nodes here#

#     def request_link(self, other):
#         msg = packLinkRequest(self.netId)
#         self.send_message(other, msg)
