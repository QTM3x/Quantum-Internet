%load_ext autoreload
%autoreload 2

from ./ import application

class BB84(application):
    def __init__(quantumInternet):
        super().__init__(quantumInternet, locationOnNetwork = 0)
        
    def teleportQubit(qubit, receiverId):
        super().teleportQubit(qubit, receiverId)
    
    def onQubit(qubit): # a state has been teleported onto a local qubit.
        pass
    
    def initiateKeyExchange(remoteUser):
        
        if success:
            print(key)
            
        pass
