import socket
import os
from _thread import *

ServerSocket = socket.socket()
serverName = '10.0.0.3'
serverPort = 12000
serverPort2 = 12001
ThreadCount = 0
try:
    ServerSocket.bind((serverName, serverPort))
    ServerSocket.bind((serverName, serverPort2))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(2)


def threaded_client(connection):
    connection.send(str.encode('Server Connected'))
    while True:
        data = connection.recv(2048)
        reply = 'Server: ' + data
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()