#!/usr/bin/python3

import threading
import collections
# This class is used to coordinate the handling of messages
# among all the ClientThreads associated with it.
# The main variables are the NameMessageQueue and the NameThreadMap.

# As its name implies, the NameMessage queue holds messages and the 
# name of the ClientThread that sent it. The name is used for two purposes
# One, to attach the name of the client that sent a message to all clients that
# received the message. The second is to make sure that a message gets sent to 
# all clients associated with the room except the one that sent it.

# The NameThread map is keyed on the username of the client and has a value
# of that Client's thread.

class RoomThread(threading.Thread):


    def __init__(self, newName): 

        threading.Thread.__init__(self)
        self.RoomName              = newName;

        self.NameMessageQueue      = collections.deque() 
        self.NotEmpty              = threading.Condition(threading.RLock()) 

        self.NameThreadMap         = {} 
        self.NameThreadMapLock     = threading.RLock() 
   
    # The main loop 
    def run(self):

        def condition():
            return len(self.NameMessageQueue) > 0 

        # Spin in a loop waiting for incoming messages
        while True:

            with self.NotEmpty:

                self.NotEmpty.wait_for(condition)

                # For each message: Go through each user and send the message
                while len(self.NameMessageQueue) != 0:
                    CurrentNameMessage = self.NameMessageQueue.pop()
#
                    with self.NameThreadMapLock:

                        for name, thread in self.NameThreadMap.items():

                            # Don't broadcast a message back to the same client that sent it.
                            if name != CurrentNameMessage[0]:
                                # There is something wrong with the client connection.
                                # Do nothing, the removal of the client will be taken care of via
                                # The RemoveClient method

                                try:
                                    thread.SendToClient(CurrentNameMessage[1])
                                except IOError as e:
                                    pass


    # This method is called by the MainServer when a request to join 
    # a particular chatroom is made.
    def AddClient(self, user):
        with self.NameThreadMapLock:
            self.NameThreadMap[user.name] = user


    # Adds a message to the MessageQueue. 'name' refers to the name of the
    # client that sent it.

    def AddMessage(self, name, message):
        assert(isinstance(name, str))
        assert(isinstance(message, str))

        with self.NotEmpty:

            self.NameMessageQueue.appendleft((name,message));
            self.NotEmpty.notify()

    # Does this room have a client with the given name?

    def HasName( self, name):
        assert(isinstance(name, str))
        with self.NameThreadMapLock:
            return name in self.NameThreadMap


    # This method is called by client threads upon receiving an IOException
    # from their socket.
    def RemoveClient( self, name):
        assert(isinstance(name, str))
        with self.NameThreadMapLock:
            del self.NameThreadMap[name]

        self.AddMessage("","<"+name+" has left the room>")


