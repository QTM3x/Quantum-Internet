%load_ext autoreload
%autoreload 2

from ../3_The_Network_Layer import repeaterChain

class quantumInternet(object):
    def __init__(self, length):
        self.parentApplication = parentApplication
        self.repeaterChain = repeaterChain(length)
        self.userTable = {}

    def requestLink(self, targetUserId, connectionParams = [#minimum fidelity and stuff#]):
        msg = packLinkReady
        self.sendMessage(parentApplication, msg)
        pass 
        
    def checkIsOnline(self, username):
        return #username in self.userTable

    def sendMessage(self, obj, msg):
        obj.handleMessage(msg)

    def handleMessage(self, msg):
        pass
