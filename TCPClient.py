from socket import *


serverName = '10.0.0.3'
serverPort = 12013
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((serverName,serverPort))
except socket.error as e:
    print(str(e))

while True:
    message = clientSocket.recv(1024)
    print(message.decode())
    user_input = input('Enter message to send to server: ')
    clientSocket.send(user_input.encode())
    response = clientSocket.recv(1024)
    print(response.decode())
    break

    print(str(e))

clientSocket.close()
