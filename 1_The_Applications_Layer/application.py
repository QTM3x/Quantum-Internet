%load_ext autoreload
%autoreload 2

class application(object): # this code runs on the user's PQC (personal quantum computer)
    def __init__(self, username = None):
        self.quantumInternet = None
        this.username = username
        # endnode is the node the application is running on
        self.endode = endnode() 

    def teleportQubit(qubit, remoteUser):
        # check if we have a link with receiverId
        # if we don't have one, request one
        self.quantumIntenet.requestLink("Bob")
        # send the classical bits to Bob
        qInternet.text("Bob", "bits are " + ...)
