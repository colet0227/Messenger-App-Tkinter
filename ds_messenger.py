# ICS 32 Winter 2022
# Final Project
#
#
# Cole Thompson / Nathan Yang
# cwthomps@uci.edu / npyang@uci.edu
# 36762668 / 63942782
import ds_client

class DirectMessage:
    """
    This class is responsible for setting attributes for the initialized object.
    """

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    This class is responsible for communicating to the server and sets attributes for the initialized object.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
    

    def send(self, message:str, recipient:str) -> bool:
        """
        Utilizes the ds_client send function to send a message to a recipient.
        : returns true if message successfully sent, false if send failed.
        """
        check = ds_client.send(self.dsuserver, 3021, self.username, self.password, message, recipient, choices = 1)
        return check
        

    def retrieve_new(self) -> list:
        """
        Utilizes the ds_client send function to gain access to new messages that the user has received.
        : returns a list of DirectMessage objects containing all new messages
        """
        direct_message_list = []
        obj_list = ds_client.send(self.dsuserver, 3021, self.username, self.password, choices = 2)
        try:
            for val in obj_list:
                # Instantiates the DirectMessage Class
                obj = DirectMessage()
                # Assigns the recipient attribute
                obj.recipient = val['from']
                # Assigns the message attribute
                obj.message = val['message']
                # Assigns the timestamp attribute
                obj.timestamp = val['timestamp']
                
                direct_message_list.append(obj)
        except:
            pass
        return direct_message_list


    def retrieve_all(self) -> list:
        """
        Utilizes the ds_client send function to gain access to all messages that the user has received.
        : returns a list of DirectMessage objects containing all messages
        """
        direct_message_list = []
        obj_list = ds_client.send(self.dsuserver, 3021, self.username, self.password, choices = 3)
        for val in obj_list:
            # Instantiates the DirectMessage Class
            obj = DirectMessage()
            # Assigns the recipient attribute
            obj.recipient = val['from']
            # Assigns the message attribute
            obj.message = val['message']
            # Assigns the timestamp attribute
            obj.timestamp = val['timestamp']
            
            direct_message_list.append(obj)
        
        return direct_message_list
