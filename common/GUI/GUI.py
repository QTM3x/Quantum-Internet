
from IPython.display import clear_output

def init():
    global gui
    gui = GUI()

class GUI(object):
    def __init__(self):
        self.request_queue = []
        self.busy = False
        self.shutdown_flag = False
        self.message = ""
        
    def draw_state(self, state):
        t1 = ""
        t2 = ""
        s = ""
        for i in range(len(state)):
#             s = s + "r" + "[" + str(i+1) + "]"
            s = s + "r"
            if i < len(state) - 1:
                if int(state[i]) == i + 1:
                    s += " ---- "
                    t1 += "  " + "    " + " "
                    t2 += "  " + "    " + " "
                else:
                    s += "      "
                    if state[i] != -1:
                        t1 += " /" + (int(state[i])-i-1) * ("    " + "   ") + "    " + "\\"
                        t2 += "  " + (int(state[i])-i-1) * ("----" + "---") + "----" + " "
                    else: 
                        t1 += "  " + "    " + " "
                        t2 += "  " + "    " + " "
#         if int(state[0]) == len(state)-1:
#             s += "       Success!"
        clear_output(wait = True)
        print(t2)
        print(t1)
        print(s)
        if self.message != "":
            print("message: ", self.message)
        if self.shutdown_flag:
            print("shutting down GUI ...")
        
    def update_gui(self, repeater_chain):
        snapshot = self.pack_snapshot(repeater_chain)
        self.request_queue.append(snapshot)
        if self.busy == False and self.shutdown_flag == False:
            self.get_busy()
#             threading.Thread(target = self.get_busy, args = ()).start()
        
    def get_busy(self):
        self.busy = True
        while len(self.request_queue) > 0:
            new_state = self.request_queue.pop(0)
            self.draw_state(new_state)
        self.busy = False 
        
    def set_message(self, message):
        self.message = message
        
    # Says which link each link is connected to.
    def pack_snapshot(self, repeater_chain):
        snapshot = []  
        for repeater in repeater_chain.repeaters:
            if repeater.rightNode is not None:
                snapshot.append(repeater.rightNode.id)
            else:
                # -1 means it's not linked to any repeaters.
                snapshot.append(-1)
#         print(snapshot)
        return snapshot
        
    def shutdown(self):
        print("shutting down GUI ...")
        self.shutdown_flag = True
