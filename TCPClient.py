from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname
serverName = 'put your hostname here'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)

print ('From Server:', modifiedSentence.decode())
clientSocket.close()
