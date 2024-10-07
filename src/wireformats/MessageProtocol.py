
from enum import Enum

class MessageProtocol(Enum):
    REGISTER_REQUEST = 0
    REGISTER_RESPONSE = 1
    
    DEREGISTER_REQUEST = 2
    DEREGISTER_RESPONSE = 3
    
    INVITATION_REQUEST = 4
    INVITATION_RESPONSE = 5

    value = None # A Message Protocol has an integer value associated with it

    def __init__(self, value):
        self.value = value
    
    def getValue(self):
        return self.value 

