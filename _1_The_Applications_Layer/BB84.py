
import sys

sys.path.append(".")
from random import SystemRandom

from .application import Application

class BB84(Application):
    def __init__(self, quantum_internet, username):
        super().__init__(quantum_internet, username)
        self.RNG = SystemRandom() # a high quality random number generator

    def send_qubit(self, qubit, remote_user):
        super().send_qubit(self, qubit, remote_user)

    def receive_qubit(qubit): # a state has been teleported onto a local qubit.
        measure # that's why you need to create an endNode object in the link layer.
        pass

    def initiate_key_exchange(self, remote_user, n=10):
        # check that the user is connected to the network.
        if not self.quantum_internet.check_IsOnline(remote_user):
            return
        basis_bits = self.randomBits(n)
        key_bits = self.randomBits(n)
        for (key,basis) in zip(key_bits,basis_bits):
            if basis == 0:
                self.send_qubit(basis(2,key))
            else:
                self.send_qubit(H * basis(2,key))
            # wait for the remoteUser to acknowledge receipt and measurement

    def send_bases(self, remote_user, basis_bits):
        msg = {'msg' : "forward to user",
               'sender' : this.username, 
               'receiver' : remoteUser,
               'type' : "basis bits",
               'data' : basisBits}
        self.send_message(self.quantum_internet, msg)

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        if msg['msg'] == "msg from user":
            if msg['type'] == "basis bits":
                self.received_bases(msg['data'])

    def received_bases(self, bases):
        pruned_key_bits = []
        for i in range(len(bases)):
            if bases[i] == basis_bits[i]:
                pruned_key_bits.append(key_bits[i])
        self.handle_exchange_complete()
        
    def handle_exchange_complete(self):
        print(key)

    def check_IfEve(self, pruned_key_bits):
        # tests some bits of the key at random to check
        # if there was an eavesdropper.
        pass

    def randomBits(self, n):
        return [self.RNG.randrange(2) for i in range(n)]
