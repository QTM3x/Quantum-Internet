%load_ext autoreload
%autoreload 2

from ../4_The_Link_Layer import repeater

class repeaterChain(object):
    def __init__(length):
        self.repeaters = [new repeater() for _ in range(length)]
    
    def attemptSwap(self, repeater):
        #ask repeater to do a swap
        repeater.attemptSwap(#specify the links to swap#)
    
    def attemptLinkCreation(self, repeater1, repeater2):
        repeater1.attemptLinkCreation(repeater2)
