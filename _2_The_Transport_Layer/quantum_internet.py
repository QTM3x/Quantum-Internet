import sys

sys.path.append("..")
from _3_The_Network_Layer.repeater_chain import RepeaterChain
from common.global_state_container import global_state_container

class QuantumInternet(object):
    def __init__(self, length):
#         self.parentApplication = parentApplication
        global_state_container.init()
        self.repeater_chain = RepeaterChain(length)
        self.user_table = {} # for our 2 user network this table can have 
                            # at most 2 users. In front of each username goes the
                            # user's application object (BB84 object).

#     def requestLink(self, username, fidelity=0):
#         msg = packLinkReady
#         self.sendMessage(parentApplication, msg)
#         pass 
        
    def check_IsOnline(self, username):
        return username in self.user_table
        
    def connect(self, application):
        application.quantum_internet = self
        self.repeater_chain.connect(application.endnode)
        self.user_table.update({application.username : application})

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        if msg['msg'] == "forward to user":
            msg['msg'] = "msg from user"
            self.send_message(self.user_table[msg.receiver], msg)
