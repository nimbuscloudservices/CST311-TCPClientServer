import socket
import time
import os
import threading

ServerSocket = socket.socket()
serverName = '10.0.0.3'
serverPort = 12013
ThreadCount = 0
count = 0
message = 'From Server: '

print('Waiting for 2 Connections..\n')
try:
    ServerSocket.bind((serverName, serverPort))
except socket.error as e:
    print(str(e))

ServerSocket.listen(2)

def threaded_client(client, address, name):
    global count

    while True:
      if ThreadCount == 2:
        client.send(str.encode('From Server: Client ' + name + ' connected'))
        break

    while True:
      reply = client.recv(2048).decode()
      count += 1
      break

    print('Client ' + name + ' sent message ' + str(count) + ': ' + reply)
    clientMessage(name, reply, count)

    while True:
      if count == 2:
        client.send(message.encode())
        break

def clientMessage(name, reply, count):
    global message

    if count == 1:
      message += name + ': ' + reply
    if count == 2:
      message += ' received before ' + name + ': ' + reply

while True:
    client, address = ServerSocket.accept()
    ThreadCount += 1

    if ThreadCount == 1:
      print('Accepted first connection, calling it client ' + chr(ThreadCount+87))
      t1 = threading.Thread(target=threaded_client, args=(client, address, chr(ThreadCount+87)))
    elif ThreadCount == 2:
      print('Accepted second connection, calling it client ' + chr(ThreadCount+87) + '\n')
      t2 = threading.Thread(target=threaded_client, args=(client, address, chr(ThreadCount+87)))
      print('\n')
      print('Waiting to receive messages from client X and client Y....\n')
      t1.start()
      t2.start()
      t1.join()
      t2.join()
      break

print('\n')
print('Waiting a bit for clients to close their connection')
time.sleep(2)
print('Done')

ServerSocket.close()
