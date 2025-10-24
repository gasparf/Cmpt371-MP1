from socket import *

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)
print ('The server is ready to receive')

# insert HTTP responses for code 200, 403


while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()
     
     # Send the reply
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())
     
     # Close connection to client (but not welcoming socket)
     connectionSocket.close()
