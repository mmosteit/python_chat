#!/usr/bin/python3

from PyQt4 import QtCore
from PyQt4 import QtNetwork
import UTF8Socket
import sys
import time

# This exception is raised when the user
# asks for a chatroom that does not exist
class RoomException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

# This exception is raised when the user
# asks for a username that is already taken
class UserNameException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class ClientGuiConnection(QtCore.QThread):

    ReceivedSignal = QtCore.pyqtSignal(str)

    def __init__(self, ip, chatroom, username, gui):
        QtCore.QThread.__init__(self)
        assert(isinstance(ip, str))


        self.gui = gui

        # May throw an IOError that will be dealt with by caller
        try:
            self.sock = UTF8Socket.UTF8Socket(ip)

        except IOError:
            raise IOError("Error could not connect to the server. Please verify server is running on ip address specified and try again.")

        

        try:
            self.sock.SendMessage(chatroom)
            response = self.sock.ReceiveMessage()
   
            if response != "ACCEPTED":

                raise RoomException("Room "+chatroom+" does not exist") 

        except IOError:
            raise IOError("Connection to server has been interrupted. Please verify server is running correctly and try again")


        try:
            self.sock.SendMessage(username)

            response = self.sock.ReceiveMessage()

            if response != "ACCEPTED":

                raise UserNameException("Username "+username+" already taken")

        except IOError:
            raise IOError("Connection to server has been interrupted. Please verify server is running correctly and try again")

    #finished = QtCore.pyqtSignal(str)

    def run(self):


        self.ReceivedSignal.connect(self.gui.DisplayMessage)

        while True:
           
            try: 
                message = self.sock.ReceiveMessage()
                self.ReceivedSignal.emit(message)

            except IOError as e:
                
                self.ReceivedSignal.emit("Connection to the server has been interrupted. Please verify the server is running correctly and try again") 
                return

    def SendMessage(self, message):
        self.sock.SendMessage(message)    



if __name__ == '__main__':


    print(sys.argv)

    ClientConnection = ChatWorker(sys.argv[1]) 

    result = ClientConnection.InitiateConnection('default', 'snake')
