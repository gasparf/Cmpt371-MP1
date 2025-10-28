from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

request_line = b"GET / HTTP/1.1\r\n"
headers = b"Host: " + serverName.encode() + b"\r\n"
headers += b"User-Agent: CustomClient/1.0\r\n"
headers += b"\r\n"

full_request = request_line + headers

clientSocket.send(full_request)

modifiedSentence = clientSocket.recv(1024)

print ('From Server:', modifiedSentence.decode())

clientSocket.close()