#TCPCapitalizationServer.py
from socket import *
serverPort = 12000

# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP
packets serverSocket = socket(AF_INET,SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1) 
print('The server is ready to receive')

while True:
     connectionSocket, addr = serverSocket.accept()
     sentence = connectionSocket.recv(1024).decode()
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())

connectionSocket.close()
