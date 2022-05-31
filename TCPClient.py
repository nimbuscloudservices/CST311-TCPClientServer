from socket import *


serverName = '127.0.1.1'
serverPort = 12013
client_socket = socket(AF_INET, SOCK_STREAM)

try:
    client_socket.connect((serverName, serverPort))
except socket.error as e:
    print(str(e))

print("[CLIENT] Successfully connected to Server.")

while True:
    message = client_socket.recv(1024)
    print(message.decode())
    user_input = input('[CLIENT] Enter message to send to server: ')
    client_socket.send(user_input.encode())
    response = client_socket.recv(1024)
    print(response.decode())
    break

    print(str(e))

client_socket.close()
print("[CLIENT] Succesfully connected to Server.")