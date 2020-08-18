import sys

from random import SystemRandom

sys.path.append(".")
from .application import Application

class BB84(Application):
    def __init__(self, username):
        super().__init__(username)
        self.RNG = SystemRandom() # a high quality random number generator
        self.basis_bits = []
        self.prekey_bits = []
        self.key_bits = []
        self.bases_sent = False

    def send_qubit(self, remote_user):
        super().send_qubit(remote_user)

    def receive_qubit(self, qubit): # a state has been teleported onto a local qubit.
        print("received qubit", qubit)
        super().receive_qubit(qubit)
        # measure
        return

    def send_bases(self, remote_user):
        msg = {'msg' : "forward to user",  # this is the standard. Document it somewhere.
               'sender' : self.username, 
               'receiver' : remoteUser,
               'type' : "basis bits",
               'data' : self.basis_bits}
        self.send_message(self.quantum_internet, msg)
        
    def receive_bases(self, bases):
        for i in range(len(bases)):
            if bases[i] == self.basis_bits[i]:
                self.key_bits.append(self.prekey_bits[i])
        self.handle_exchange_complete()

    def initiate_key_exchange(self, remote_user, n=10):
        # check that the user is connected to the network.
        if not self.quantum_internet.check_IsOnline(remote_user):
            print("user", remote_user, "is not connected to the network.")
            return
        self.basis_bits = self.randomBits(n)
        self.prekey_bits = self.randomBits(n)
        for (prekey,basis) in zip(prekey_bits,basis_bits):
            if basis == 0:
                self.send_qubit(basis(2,prekey), remote_user)
            else:
                self.send_qubit(H * basis(2,prekey), remote_user)
            # wait for the remoteUser to acknowledge receipt and measurement

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        if msg['msg'] == "msg from user":
            if msg['type'] == "basis bits":
                self.receive_bases(msg['data'])
                if not self.bases_sent:
                    self.send_bases(msg['sender'])
            if msg['type'] == "qubits received":
                self.send_bases(msg['sender'])

    def handle_exchange_complete(self):
        print("Key exchange complete:", key)

    def check_IfEve(self, pruned_key_bits):
        # tests some bits of the key at random to check
        # if there was an eavesdropper.
        pass

    def randomBits(self, n):
        return [self.RNG.randrange(2) for i in range(n)]
