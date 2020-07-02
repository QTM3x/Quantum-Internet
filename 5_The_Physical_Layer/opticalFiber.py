
class opticalFiber(object):
    def __init__(self, node1, node2, length=1):
#         self.id = None
        # The length of the fiber.
        self.length = length
        # The two nodes at the two ends of the fiber.
        # A node can be a repeaterHardware, an end node, a heralding station, 
        # etc. For now it's a repeaterHardware object for simplicity.
        self.node1 = node1
        self.node2 = node2
        self.photon12 = photon(self)   # this is the photon going from node 1 to node 2
        self.photon21 = photon(self)
        global globalState
        self.globalState = globalState

    def carryPhoton(photon, sender, receiver):  # Here there will be a quantum channel applied to the state
        # apply channel here
        # for now make it the identity channel
        gate = tensor([identity(2) for _ in range(globalState.N)])
        newState = gate * self.globalState.state * gate.dag()  # for now the map is a identity unitary gate
        self.globalState.updateState(newState)
        # send output state to the receiver
        receiver.receivePhoton()
