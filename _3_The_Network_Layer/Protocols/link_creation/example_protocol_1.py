import sys

sys.path.append("..")

class ExampleProtocol1(object):
    def __init__(self, repeater_chain):
        self.name = "example protocol 1"
        self.repeater_chain = repeater_chain

    def send_message(self, obj, msg):
        obj.handle_message(msg)
    
    def handle_message(self, msg):
        if msg['msg'] == "network layer: Link request received.":
            self.initiate_link_creation(msg['endnode1'], msg['endnode2'], msg['minimum_fidelity'])

    def initiate_link_creation(self, endnode1, endnode2, minimum_fidelity=1):
        print("initiating link creation using protocol", self.name)
        chain = self.repeater_chain
        for i in range(len(chain.repeaters)-1):
            chain.repeaters[i].attempt_link_creation(chain.repeaters[i+1])
        # Also ask the link layer for links between the endnodes and the
        # edge repeaters.
        # First we get the repeater that's wired to each endnode
        endnode1_repeater = chain.repeaters[0] if endnode1.lower_cable == chain.repeaters[0].left_lower_cable else chain.repeaters[-1]
        endnode2_repeater = chain.repeaters[0] if endnode2.lower_cable == chain.repeaters[0].left_lower_cable else chain.repeaters[-1]
        # Then we link them.
        endnode1.attempt_link_creation(endnode1_repeater)
        endnode2.attempt_link_creation(endnode2_repeater)
        # Then we swap.
        for i in range(len(chain.repeaters)):
            chain.repeaters[i].attempt_swap(chain.repeaters[i].left_lower_link, chain.repeaters[i].right_lower_link)
