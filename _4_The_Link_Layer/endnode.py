import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.endnode_hardware import EndnodeHardware
print("imported EndnodeHardware object", EndnodeHardware)
from _4_The_Link_Layer.link import Link
print("imported Link object", Link)

class Endnode(object):
    def __init__(self):
        print("creating new endnode")
        self.netId = None
        self.hardware = EndnodeHardware(self)
        self.link = None
        self.cable = None
        self.parent_application = None
        self.send_flag = False
        
    def connect_cable(self, cable):
        print("connecting cable in endnode")
        self.cable = cable
        self.hardware.connect_fiber(cable.optical_fiber)
        cable.connect_node(self)

    def teleport_qubit(self):
        self.hardware.teleport_qubit()

    # attempt to create link with another repeater
    def attempt_link_creation(self, node):
        # prepare a link layer Link object.
        if self.cable is None:
            print("link creation failed: no cables connected.")
            return
        else:
            if node in (self.cable.node1, self.cable.node2):
                self.link = Link()
                self.link.node1 = self
            else:
                print("link creation failed: not connected to node.")
                return
        
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
        if msg['msg'] == "quantum internet: Link to remote user created.":
            if self.send_flag:
                self.teleport_qubit()
                self.send_flag = False
        elif msg['msg'] == "child hardware: Teleport done. Handle corrections.":
            # give the measurement results to the quantum internet, 
            # because I guess the quantum internet still has to do some
            # stuff.
            msg = {'msg' : "endnode: Teleport done. Handle corrections.",
                   'measurement_result1' : msg['measurement_result1'],
                   'measurement_result2' : msg['measurement_result2'],
                   'sender_node' : self,
                   'receiver_node' : self.link.node1 if self == self.link.node2 else self.link.node2}
            self.send_message(
                self.parent_application.quantum_internet,
                msg
            )
        elif msg['msg'] == "quantum internet: Teleport done. Handle corrections.":
            self.hardware.apply_teleport_corrections(msg['measurement_result1'], 
                                                       msg['measurement_result2'])
        elif msg['msg'] == "child hardware: Teleport corrections applied.":
            # notify the parent application that it has received a qubit
            msg = {'msg' : "child endnode: Qubit received."}
            self.send_message(self.parent_application, msg)

#    def handle_link_creation_success(self, other):
#        self.link = other

#     def handle_link_request(self):
#         # determine if the other repeater is on the left or right
            
#         # check if there is a node available on that side 
            
#         if slotAvailable:
#             # create the link
#             self.attempt_link_creation() #specify nodes here#

#     def request_link(self, other):
#         msg = packLinkRequest(self.netId)
#         self.send_message(other, msg)
