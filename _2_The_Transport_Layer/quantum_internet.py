import sys

sys.path.append("..")
from _3_The_Network_Layer.repeater_chain import RepeaterChain
from common.global_state_container import global_state_container

class QuantumInternet(object):
    def __init__(self, length):
        print("creating quantum internet")
#         self.parentApplication = parentApplication
        global_state_container.init()
        self.repeater_chain = RepeaterChain(length, self)
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
        print("connecting application (endnode) to quantum internet")
        application.quantum_internet = self
        self.repeater_chain.connect(application.endnode)
        self.user_table.update({application.username : application})
        print("new user added to user table:", self.user_table)
        
    # def send_qubit(self, qubit, sender_username, receiver_username): # do async and await here?
    #     # ask the network layer to set up a link between the two users.
    #     endnode1 = self.user_table[sender_username].endnode
    #     endnode2 = self.user_table[receiver_username].endnode
    #     # await network layer link creation
    #     self.repeater_chain.attempt_link_creation(endnode1, endnode2)
    #     # after the link has been created repeater_chain (network layer) 
    #     # should notify quantum_internet (transport layer), and then 
    #     # quantum_internet will teleport the qubit.

    def request_link(self, sender_username, receiver_username): # do async and await here?
        print("requesting link in quantum internet")
        # ask the network layer to set up a link between the two users.
        endnode1 = self.user_table[sender_username].endnode
        endnode2 = self.user_table[receiver_username].endnode
        # await network layer link creation
        self.repeater_chain.request_link(endnode1, endnode2)
        # after the link has been created repeater_chain (network layer) 
        # should notify quantum_internet (transport layer), and then 
        # quantum_internet will teleport the qubit?
    
    # def transport_qubit(self, qubit, sender_endnode, receiver_endnode):
    #     return

    def send_message(self, obj, msg):
        obj.handle_message(msg)

    def handle_message(self, msg):
        print("quantum internet received message:", msg['msg'])
        if msg['msg'] == "network layer: Link to remote endnode created.":
            # check if the nodes have a pending transport request
            # ...
            # then transport qubit
            # self.transport_qubit(qubit, msg['endnode1'], msg['endnode1'])
            msg['msg'] = "quantum internet: Link to remote user created."
            self.send_message(msg['endnode1'], msg)
            self.send_message(msg['endnode2'], msg)
        elif msg['msg'] == "endnode: Teleport done. Handle corrections.":
            msg['msg'] = "quantum internet: Teleport done. Handle corrections."
            self.send_message(msg['receiver_node'], msg)
        # elif msg['msg'] == "forward to user":
        #     msg['msg'] = "msg from user"
        #     self.send_message(self.user_table[msg.receiver], msg)
        else:
            print("quantum internet received unknown message \"" + msg['msg'] + "\"")
