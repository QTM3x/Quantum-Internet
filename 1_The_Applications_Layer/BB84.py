%load_ext autoreload
%autoreload 2

from random import SystemRandom

from ./ import application

class BB84(application):
    def __init__(self, quantumInternet, username):
        super().__init__(quantumInternet, username)
        self.RNG = SystemRandom() # a high quality random number generator

    def teleportQubit(qubit, remoteUser):
        super().teleportQubit(qubit, remoteUser)

    def onQubit(qubit): # a state has been teleported onto a local qubit.
        measure # that's why you need to create an endNode object in the link layer.
        pass

    def initiateKeyExchange(self, remoteUser, noOfBits=10):
        # check that the user is connected to the network.
        if !self.quantumInternet.checkIsOnline(remoteUser):
            return
        basisBits = self.randomBits(noOfBits)
        keyBits = self.randomBits(noOfBits)
        for (key,basis) in zip(keyBits,basisBits):
            if basis == 0:
                self.teleportQubit(basis(2,key))
            else:
                self.teleportQubit(H * basis(2,key))
            # wait for the remoteUser to acknowledge receipt and measurement

    def sendBases(self, remoteUser, basisBits):
        msg = {'msg' : "forward to user",
               'sender' : this.username, 
               'receiver' : remoteUser,
               'type' : "basis bits,"
               'data' : basisBits}
        self.sendMessage(self.quantumInternet, msg)

    def sendMessage(self, obj, msg):
        obj.handleMessage(msg)

    def handleMessage(self, msg):
        if msg['msg'] == "msg from user":
            if msg['type'] == "basis bits":
                self.handleReceivedBases(msg['data'])

    def handleReceivedBases(self, bases):
        prunedKeyBits = []
        for i in range(len(bases)):
            if bases[i] == basisBits[i]:
                prunedKeyBits.append(keyBits[i])
        self.handleExchangeComplete()
        
    def handleExchangeComplete(self)
        print(key)

    def checkIfEve(self, prunedKeyBits):
        # tests some bits of the key at random to check
        # if there was an eavesdropper.
        pass

    def randomBits(self, noOfBits):
        return [self.RNG.randrange(2) for i in range(noOfBits)]
