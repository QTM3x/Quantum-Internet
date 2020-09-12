import sys

sys.path.append("..")
from _5_The_Physical_Layer.node_hardware.endnode_hardware import EndnodeHardware
from _4_The_Link_Layer.link import Link

class Endnode(object):
    def __init__(self):
        print("creating new endnode")
        self.netId = None
        self.hardware = EndnodeHardware(self)
        self.upper_link = None
        self.lower_link = None
        self.upper_cable = None
        self.lower_cable = None
        self.parent_application = None
        self.parent_repeater_chain = None
        self.send_flag = False

    def connect_cable(self, cable, upper_or_lower="lower"):
        print("connecting " + upper_or_lower + " cable in endnode")
        if upper_or_lower == "upper":
            self.upper_cable = cable
        else:
            self.lower_cable = cable
        self.hardware.connect_fiber(cable.optical_fiber, upper_or_lower)
        cable.connect_node(self)

    def teleport_qubit(self): # teleport using the lower qubit
        # ask the hardware to execute the teleportation circuit
        self.hardware.teleport_qubit()
        # destroy link involved in teleport
        self.lower_link = None

    # attempt to create link with another repeater
    def attempt_link_creation(self, remote_node, upper_or_lower="lower"):
        print("attempting " + upper_or_lower + " link creation in endnode")
        # prepare a link layer Link object.
        if self.lower_cable is None and self.upper_cable is None:
            print("link creation failed: no cables connected.")
            return
        else:
            if upper_or_lower == "lower":
                if remote_node in (self.lower_cable.node1, self.lower_cable.node2):
                    self.lower_link = Link()
                    self.lower_link.node1 = self
                else:
                    print("not connected to node via lower cable")
                    return
            else:
                if remote_node in (self.upper_cable.node1, self.upper_cable.node2):
                    self.upper_link = Link()
                    self.upper_link.node1 = self
                else:
                    print("not connected to node via upper cable")
                    return
        # attempt link creation on the next free qubit
        self.hardware.attempt_link_creation(remote_node.hardware, upper_or_lower)

    # attempt to do entanglement distillation of 
    # two links with the same repeater.
    def attempt_distillation(self, link1, link2):
        self.hardware.attempt_distillation()

    # this function emits a signal to the link layer (which here takes the form 
    # of software running on the repeater).
    def send_message(self, obj, msg):
        obj.handle_message(msg)

    # this function receives an emitted signal
    def handle_message(self, msg):
        print("endnode with netId", str(self.netId), "received message:", msg['msg'])
        if msg['msg'] == "quantum internet: Link to remote user created.":
            endnode1 = msg['endnode1']
            endnode2 = msg['endnode2']
            # print("DEBUG: in endnode. Node of created end to end link are", endnode1, endnode2)
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
                   'receiver_node' : self.lower_link.node1 if self == self.lower_link.node2 else self.lower_link.node2}
            self.send_message(
                self.parent_application.quantum_internet,
                msg
            )
            # teleportation uses up the link
            self.lower_link = None
        elif msg['msg'] == "quantum internet: Teleport done. Handle corrections.":
            self.hardware.apply_teleport_corrections(msg['measurement_result1'], 
                                                       msg['measurement_result2'])
        elif msg['msg'] == "child hardware: Teleport corrections applied.":
            # notify the parent application that it has received a qubit
            msg = {'msg' : "child endnode: Qubit received."}
            # destroy the link with the endnode that sent the qubit
            self.lower_link = None
            # notify the parent application
            self.send_message(self.parent_application, msg)
        elif msg['msg'] == "child hardware: Entanglement swapping corrections applied.":
            return
        elif msg['msg'] == "neighbor repeater: Entanglement swapping done. Handle corrections.":
            self.hardware.apply_swap_corrections(msg['measurement_result1'], 
                                            msg['measurement_result2'])
        elif msg['msg'] == "child hardware: Received qubit.":
            return
        elif msg['msg'] == "child hardware: Received link qubit.":
            sender = msg['sender']
            upper_or_lower = msg['upper_or_lower']
            link = msg['link']
            link.node2 = self
            if upper_or_lower == "upper":
                self.upper_link = link
            else:
                self.lower_link = link
            # notify the parent repeater chain?
            if self.parent_repeater_chain:
                msg = {'msg' : "child endnode: Link created.",
                       'upper_or_lower' : upper_or_lower,
                       'link': self.upper_link if upper_or_lower=="upper" else self.lower_link
                       }
                self.send_message(self.parent_repeater_chain, msg)
        elif msg['msg'] == "child hardware: Sent link qubit.":
            return
        else:
            print("endnode received unknown message \"" + msg['msg'] + "\"")
