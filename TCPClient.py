from socket import *


serverName = '10.0.0.3'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

print('Waiting for connection')
try:
    clientSocket.connect((serverName,serverPort))
except socket.error as e:
    print(str(e))


while True:
    user_input = input('Say Something: ')
    clientSocket.send(user_input.encode())
    response = clientSocket.recv(1024)
    print(response)

clientSocket.close()



