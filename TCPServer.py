import socket
import os
from _thread import *

ServerSocket = socket.socket()
serverName = '10.0.0.3'
serverPort = 12013
ThreadCount = 0

print('Waitiing for 2 Connections..')
try:
    ServerSocket.bind((serverName, serverPort))
except socket.error as e:
    print(str(e))

ServerSocket.listen(2)


def threaded_client(connection):
    connection.send(str.encode('Server Connected: ' ))
    while True:
        reply = connection.recv(2048).decode()    
        connection.send(reply.encode())  
    connection.close()

while True:
    client, address = ServerSocket.accept()
    start_new_thread(threaded_client, (client, ))
    
    ThreadCount += 1
    
    print('Accepted first connection, calling it client: ', ThreadCount)

ServerSocket.close()


