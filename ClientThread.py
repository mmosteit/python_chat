#!/usr/bin/python3
import threading


class ClientThread(threading.Thread):

    def __init__(self, newRoom, newSock, newName):
        threading.Thread.__init__(self)
        self.sock = newSock
        self.room = newRoom
        self.name = newName
    

    def run(self):
        
        # spin while waiting on a message
        while True:

            try:

                # Read in a message and send it to the chatroom's message queue
                message = self.sock.ReceiveMessage()
                
                # Name is required as the first parameter so that the server
                # can know not to relay the message back to the client that
                # said it.
                self.room.AddMessage(self.name, self.name+": "+message)

            except IOError as e:
                self.room.RemoveClient(self.name)
                return
    
            except Exception as e:
                self.room.RemoveClient(self.name)
                return           
 
    # This method is called by the room thread
    def SendToClient(self, message):
        self.sock.SendMessage(message)
