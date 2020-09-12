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
        self.left_upper_link = None
        self.left_lower_link = None
        self.right_upper_link = None
        self.right_lower_link = None
        self.left_upper_cable = None
        self.left_lower_cable = None
        self.right_upper_cable = None
        self.right_lower_cable = None

    def connect_right_cable(self, cable, upper_or_lower="lower"):
        print("connecting " + upper_or_lower + " right cable in repeater")
        if upper_or_lower == "upper":
            self.right_upper_cable = cable
        else:
            self.right_lower_cable = cable
        self.hardware.connect_right_fiber(cable.optical_fiber, upper_or_lower)
        cable.connect_node(self)
        
    def connect_left_cable(self, cable, upper_or_lower="lower"):
        print("connecting " + upper_or_lower + " left cable in repeater")
        if upper_or_lower == "upper":
            self.left_upper_cable = cable
        else:
            self.left_lower_cable = cable
        self.hardware.connect_left_fiber(cable.optical_fiber, upper_or_lower)
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
    def attempt_link_creation(self, remote_node, upper_or_lower="lower"):
        print("attempting " + upper_or_lower + " link creation in repeater")
        # prepare a link layer Link object.
        if self.left_lower_cable and self.left_lower_cable.is_connected(remote_node):
            side = "left"
        elif self.left_upper_cable and self.left_upper_cable.is_connected(remote_node):
            side = "left"
        elif self.right_lower_cable and self.right_lower_cable.is_connected(remote_node):
            side = "right"
        elif self.right_upper_cable and self.right_upper_cable.is_connected(remote_node):
            side = "right"
        else:
            print("not connected to remote node")
            return
        if side == "left":
            if upper_or_lower == "upper":
                self.left_upper_link = Link()
                self.left_upper_link.node1 = self
            else:
                self.left_lower_link = Link()
                self.left_lower_link.node1 = self
        else:
            if upper_or_lower == "upper":
                self.right_upper_link = Link()
                self.right_upper_link.node1 = self
            else:
                self.right_lower_link = Link()
                self.right_lower_link.node1 = self
        # ask the hardware to attempt link creation
        self.hardware.attempt_link_creation(remote_node.hardware, upper_or_lower)

    # attempt to do entanglement distillation of 
    # two links with the same repeater.
    def attempt_distillation(self, link1, link2):
        self.hardware.attempt_distillation()

    def handle_swap_success(self):
        # create new link between edge nodes and discard used up links
        # print("debug:", self.left_link, self.right_link)
        left_lower_edge_node = self.left_lower_link.node1 if self.left_lower_link.node1 != self else self.left_lower_link.node2
        right_lower_edge_node = self.right_lower_link.node1 if self.right_lower_link.node1 != self else self.right_lower_link.node2
        new_link = Link()
        new_link.node1 = left_lower_edge_node
        new_link.node2 = right_lower_edge_node
        # new_link.fidelity = ...
        # print("debug: ", left_edge_node, right_edge_node)
        if type(left_lower_edge_node).__name__ == "Endnode":
            left_lower_edge_node.lower_link = new_link
        else:
            left_lower_edge_node.right_lower_link = Link()
        if type(right_lower_edge_node).__name__ == "Endnode":
            right_lower_edge_node.lower_link = new_link
        else:
            right_lower_edge_node.left_lower_link = new_link
        # destroy links involved in swap
        self.left_lower_link = None
        self.right_lower_link = None
        #notify parent repeater chain (network layer)
        msg = {'msg' : "repeater: Swap complete.",
               'node1': left_lower_edge_node,
               'node2': right_lower_edge_node}
        self.send_message(self.parent_repeater_chain, msg)


    # this function emits a signal to the link layer (which here takes the form 
    # of software running on the repeater).
    def send_message(self, obj, msg):
        obj.handle_message(msg)

    # this function receives an emitted signal
    def handle_message(self, msg):
        print("repeater with netId", str(self.netId), "received message:", msg['msg'])
        if msg['msg'] == "child hardware: Entanglement swapping done. Handle corrections.":
            # update connections table
            self.handle_swap_success() # you're still not handling corrections.
            # retitle the message and forward it.
            # Note that the msg contains two measurement results.
            msg['msg'] = "neighbor repeater: Entanglement swapping done. Handle corrections."
            msg['sender'] = self
            remote_repeater = self.right_lower_cable.node1 if self.right_lower_cable.node1 != self else self.right_lower_cable.node2
            self.send_message(remote_repeater, msg)
        elif msg['msg'] == "neighbor repeater: Entanglement swapping done. Handle corrections.":
            measurement_result1 = msg['measurement_result1']
            measurement_result2 = msg['measurement_result2']
            sender = msg['sender']
            # assume we have received the qubit already.
            # ask the repeaterHardware to apply corrections.
            side = "left" if sender in (self.left_lower_cable.node1, self.left_lower_cable.node2) else "right"
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
            side = msg['side']
            upper_or_lower = msg['upper_or_lower']
            link = msg['link']
            link.node2 = self
            if side == "left":
                if upper_or_lower == "upper":
                    self.left_upper_link = link
                else:
                    self.left_lower_link = link
            else:
                if upper_or_lower == "upper":
                    self.right_upper_link = link
                else:
                    self.right_lower_link = link
            # notify the parent repeater chain
            if self.parent_repeater_chain:
                msg = {'msg' : "child repeater: Link created.",
                       'link': link,
                       'side': side,
                       'upper_or_lower' : upper_or_lower}
                self.send_message(self.parent_repeater_chain, msg)
        elif msg['msg'] == "child hardware: Sent link qubit.":
            return
        else:
            print("repeater received unknown message \"" + msg['msg'] + "\"")
