#!/usr/bin/python3

import socket
import threading
import RoomThread
import ClientThread
import sys
import UTF8Socket

class MainServer:

#    public  Socket connection;
#    public  ServerSocket MainSock;
#    private HashMap<String,RoomThread> RoomMap;
#    private RoomThread room;

    def __init__ (self, args):

        # Thread RoomThread_Thread;
        self.RoomThreadMap  = {}
        self.MainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.MainSock.bind((args[1],9001))
        self.MainSock.listen(3)

        # Create all chatrooms specified
        for i in range(2, len(args)):
            if  args[i] in  self.RoomThreadMap:
                pass 
            else:
                room = RoomThread.RoomThread(args[i])
                # Specifying that a thread is a daemon enables the entire program to
                # Be killed with Control -C
                room.daemon = True 
                self.RoomThreadMap[args[i]]  = room
                room.start()            
                print("Just created room ,",args[i])

    def run(self):

        print("Now waiting for connections. Press Ctrl - C to stop")

        while True:
            try:
                   
                connection, address = self.MainSock.accept()
                sock = UTF8Socket.UTF8Socket(connection)
                  
                # Get the desired room name
                RoomName = sock.ReceiveMessage()
                print(RoomName)
                if RoomName in self.RoomThreadMap:
                    room = self.RoomThreadMap[RoomName] 
                    sock.SendMessage("ACCEPTED")
                else:
                    sock.SendMessage("REJECTED")
                    sock.close()
                    continue
                        
                         
                # Get the desired username
                UserName = sock.ReceiveMessage()
                       
                         
                # Add the user to the room if it does not already contain the user
                if room.HasName(UserName) :
                    sock.SendMessage("REJECTED")
                    sock.close()
                    continue
                           
                            
                else:
                    sock.SendMessage("ACCEPTED")
                    client = ClientThread.ClientThread(room, sock, UserName)
                    client.daemon = True
                    room.AddClient(client)
                    client.start()
                    room.AddMessage("server", "<"+UserName+" has entered the room>")
                
                      
                # If an IOException occurs anywhere in the above code, then the connection
                # is bad and no operations should continue. Keep going and accept another 
                # connection.
            
            except IOError as e:
                str(e)
                sys.exit()

            except KeyboardInterrupt:
                sys.exit()


if __name__ == '__main__':


        if len(sys.argv) < 2:
            print("Error: must specify at least one chat room")
            print("ChatServer: ip_address room_list")
            print("room_list is at least one room name")
            sys.exit(1)
        
        try:
            server = MainServer(sys.argv);
            server.run()

        except socket.gaierror as e:
            print ("Could not bind to address")     
            sys.exit()
 
        except IOError as e:
            print("Constructor failed due to IOException ")
            print(str(e))
            sys.exit()

        except Exception as e:
            print("Caught a generic exception from mainserver in main method:")
            print(type(e))
            print(str(e)) 
            sys.exit()
