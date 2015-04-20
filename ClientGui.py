#!/usr/bin/python3
from PyQt4 import QtGui, QtCore, uic
import sys
import time
import ClientGuiConnection

class ClientGui(QtGui.QMainWindow):

    # This signal serves to send text to
    # the ClientGuiConnection instance.

    # For some odd reason, it must be declares as
    # a member of ClientGui rather than an instance variable    
    SendSignal = QtCore.pyqtSignal(str)

    def __init__(self):

        super(ClientGui, self).__init__()

        # Load the widgets defined in the xml file
        uic.loadUi('chat.ui', self)

        self.SendButton.clicked.connect(self.SendMessage)
        self.WriteText.returnPressed.connect(self.SendMessage)
        self.show()


    # Display a message in the chat window
    def DisplayMessage(self, message):
        self.ReadText.appendPlainText(message)


    # Send a message to the server and display it in the chat window
    # SetConnection must be called prior to this
    def SendMessage(self):

        text = self.WriteText.text()
        self.WriteText.clear()
        self.DisplayMessage('Me: '+text)   
        self.SendSignal.emit(text)


    # This associates the gui with an instance of ClientGuiConnection 
    def SetConnection(self, connection):
        self.connection = connection
        self.SendSignal.connect(self.connection.SendMessage)

    def SetTitle(self, NewTitle):
        self.setWindowTitle(NewTitle)        
 
if __name__ == '__main__':
    app    = QtGui.QApplication(sys.argv)

    if len(sys.argv) != 4:
        print("Usage: ")
        print(sys.argv[0]+" server_ip room_name username")
        sys.exit(1)


    ip_address =  sys.argv[1]
    chatroom   =  sys.argv[2]
    username   =  sys.argv[3]

    # Start the main gui
    window = ClientGui()
   
    try: 
        connection = ClientGuiConnection.ClientGuiConnection(ip_address, chatroom, username, window )

        # The connection must be started after the gui
        # So that any incoming messages are not sent to a gui
        # that does not exist.
        window.SetConnection(connection)   
        connection.start()
        window.SetTitle(username+'@'+chatroom)

    except ClientGuiConnection.RoomException as e:
        window.DisplayMessage(str(e))

    except ClientGuiConnection.UserNameException as e:
        window.DisplayMessage(str(e))

    except IOError as e:
        window.DisplayMessage(str(e)) 

    except Exception as e:
        window.DisplayMessage(str(e))

    result = app.exec_() 

    sys.exit(result)

