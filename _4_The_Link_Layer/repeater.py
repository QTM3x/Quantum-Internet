import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.repeater_hardware import RepeaterHardware
from _4_The_Link_Layer.link import Link

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
    
    def attempt_swap(self, left_link, right_link):
        print("repeater", self , ": Attempting swap.")
        if left_link == None:
            print("repeater", self , ": Swap failed. Left link missing.")
            return
        if right_link == None:
            print("repeater", self , ": Swap failed. Right link missing.")
            return    
        self.hardware.swap_entanglement()

    # attempt to create link with another node
    def attempt_link_creation(self, node):
        print("attempting link creation in repeater")
        # prepare a link layer Link object.
        if self.left_cable is None:
            if self.right_cable is None:
                print("link creation failed: no cables connected.")
                return
            else:
                if node in (self.right_cable.node1, self.right_cable.node2):
                    side = "right"
                else:
                    print("link creation failed: not connected to node", node)
                    return
        else:
            if node in (self.left_cable.node1, self.left_cable.node2):
                side = "left"
            else:
                if self.right_cable is None:
                    print("link creation failed: not connected to node.")
                    return
                else:
                    if node in (self.right_cable.node1, self.right_cable.node2):
                        side = "right"
                    else:
                        print("link creation failed: not connected to node.")
                        return
        # side = "left" if node in (self.left_cable.node1, self.left_cable.node2) else "right"
        if side == "left":
            self.left_link = Link()
            self.left_link.node1 = self
        else:
            self.right_link = Link()
            self.right_link.node1 = self
        # ask the hardware to attempt link creation
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
        if msg['msg'] == "child hardware: Entanglement swapping done. Handle corrections.":
            # update connections table
            self.handle_swap_success() # you're still not handling corrections.
            # retitle the message and forward it.
            # Note that the msg contains two measurement results.
            msg['msg'] = "neighbor repeater: Entanglement swapping done. Handle corrections."
            msg['sender'] = self
            remote_repeater = self.right_cable.node1 if self.right_cable.node1 != self else self.right_cable.node2
            self.send_message(remote_repeater, msg)
        elif msg['msg'] == "neighbor repeater: Entanglement swapping done. Handle corrections.":
            measurement_result1 = msg['measurement_result1']
            measurement_result2 = msg['measurement_result2']
            sender = msg['sender']
            # assume we have received the qubit already.
            # ask the repeaterHardware to apply corrections.
            side = "left" if sender in (self.left_cable.node1, self.left_cable.node2) else "right"
            self.hardware.apply_swap_corrections(side,
                                                       measurement_result1, 
                                                       measurement_result2)
        elif msg['msg'] == "child hardware: Entanglement swapping corrections applied.":
            # update connections table
#             self.handle_swap_success(..., ...)
            return
        elif msg['msg'] == "child hardware: Received qubit.":
            return
        elif msg['msg'] == "child hardware: Received link qubit.":
            sender = msg['sender']
            if type(sender).__name__ == "EndnodeHardware":
                remote_node = sender.parent_endnode # sender is a node hardware
            else:
                remote_node = sender.parent_repeater
            side = "left" if remote_node in (self.left_cable.node1, self.left_cable.node2) else "right"
            if side == "left":
                if type(remote_node).__name__ == "Endnode":
                    self.left_link = remote_node.link
                else:
                    self.left_link = remote_node.right_link
                self.left_link.node2 = self
            else:
                if type(remote_node).__name__ == "Endnode":
                    self.right_link = remote_node.link
                else:
                    self.right_link = remote_node.left_link
                self.right_link.node2 = self
            # notify the parent repeater chain
            if self.parent_repeater_chain:
                msg = {'msg' : "child repeater: Link created.",
                       'link': self.left_link if side == "left" else self.right_link,
                       'side': side}
                self.send_message(self.parent_repeater_chain, msg)
        elif msg['msg'] == "child hardware: Sent link qubit.":
            # receiver = msg['receiver'].parent_repeater # change this to parent node throughout
            # side = "left" if receiver in (self.left_cable.node1, self.left_cable.node2) else "right"
            # if side == "left":
            #     self.left_link = Link()
            #     self.left_link.node1 = self
            # else:
            #     self.right_link = Link()
            #     self.right_link.node1 = self
            return
        else:
            print("received unknown message")

    def handle_swap_success(self):
        # create new link between edge nodes and discard used up links
        # print("debug:", self.left_link, self.right_link)
        left_edge_node = self.left_link.node1 if self.left_link.node1 != self else self.left_link.node2
        right_edge_node = self.right_link.node1 if self.right_link.node1 != self else self.right_link.node2
        new_link = Link()
        new_link.node1 = left_edge_node
        new_link.node2 = right_edge_node
        # new_link.fidelity = ...
        # print("debug: ", left_edge_node, right_edge_node)
        if type(left_edge_node).__name__ == "Endnode":
            left_edge_node.link = new_link
        else:
            left_edge_node.right_link = Link()
        if type(right_edge_node).__name__ == "Endnode":
            right_edge_node.link = new_link
        else:
            right_edge_node.left_link = new_link
        #notify parent repeater chain (network layer)
        msg = {'msg' : "repeater: Swap complete.",
               'node1': self.left_link.node1 if self == self.left_link.node2 else self.left_link.node2,
               'node2': self.right_link.node1 if self == self.right_link.node2 else self.right_link.node2}
        self.send_message(self.parent_repeater_chain, msg)
        # destroy links involved in swap
        self.left_link = None
        self.right_link = None
        print("repeater", self , ": Swapping done.")

#     def handle_link_creation_success(self, side, remote_repeater):
#         if side == "left":
#             self.left_link = remote_repeater
#         elif side == "right":
#             self.right_link = remote_repeater
    
#    def handle_link_request(self):
#        # determine if the other repeater is on the left or right
            
#        # check if there is a node available on that side 
            
#        if slotAvailable:
#            # create the link
#            self.attempt_link_creation() #specify nodes here#
