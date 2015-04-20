#!/usr/bin/python
import socket
import struct

# This class represents a wrapper around a TCP socket. It sends and receives
# UTF-8 encoded data across a network connection. The protocol is extremely
# simple and consists of sending a signed 4 byte integer denoting the number of
# bytes in the UTF-8 string (not including the 4 byte integer), followed by the
# string itself. Given that this deals with data over a network connection. All
# outgoing and incoming data shall be in big-endian order.

class UTF8Socket():

    def __init__(self, arg):
        
        if isinstance(arg, str):
            self.sock = socket.socket()
            self.sock.connect((arg, 9001))

        elif isinstance(arg, socket.socket):
            self.sock = arg

        else:
            raise TypeError("Argument to UTF8Socket constructor is neither string nor socket")
    
    # Send 4 bytes denoting the size of the string, followed by the string
    # itself.

    def SendMessage(self, message):
        # Send message through the socket

        bytestring = message.encode() # Conver the message into a utf-8 bytestring
        length = len(bytestring)

        packedlength = struct.pack(">i",length)
        
        self.sock.send(packedlength)
        self.sock.send(bytestring)


    def ReceiveMessage(self):

        try:
            sizeBytes = self.sock.recv(4)

            # There is a problem with the connection
            
            if len(sizeBytes) == 0:
                raise IOError("There is a problem with the socket")
    
 
            while len(sizeBytes) < 4:
                oldLen = len(sizeBytes)
                sizeBytes += self.sock.recv(4 - len(sizeBytes))
                newLen = len(sizeBytes)

                # No data transmitted, there was a problem with the socket
                if oldLen == newLen: 
                    raise IOError("There is a problem with the connection. Please verify that the server is running correctly and restart program.")               
 
            size = struct.unpack(">i",sizeBytes)[0]
    
            messageBytes = self.sock.recv(size)

            while len(messageBytes) < size:
                messageBytes += self.sock.recv(size - len(messageBytes))
    
            message = messageBytes.decode()
    
            return message

        except IOError as e:
            print("IOError in UTF8Socket.receivemessage")
            raise 

    def close(self):
        self.sock.close()
