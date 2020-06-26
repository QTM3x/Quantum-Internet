
class opticalFiber(object):
    def __init__(length, node1, node2):
        self.length = length
        # The two nodes at the two ends of the fiber.
        # A node can be a repeater, a user node, a heralding station, 
        # etc.
        self.node1 = node1
        self.node2 = node2
        
    
    def carryPhoton(state, sender, receiver):  # Here there will be a quantum channel applied to the state
        # apply channel here
        
        # send output state to the receiver
        
