from socket import *
import os

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverRoot = "."

serverSocket.listen(1)
print ('The server is ready to receive')

# insert HTTP responses for code 200, 403





#404 and 200
def serve_html_file(file_name):
    file_path = os.path.join(serverRoot, file_name)
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        headers = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        return headers + content
    except FileNotFoundError:
        error_content = b"<h1>404 Not Found</h1><p>This is Yan Ting and we cannot find the requested file.</p>"
        headers = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        return headers + error_content







while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()


     #404
     #if not sentence:
     #     break

     print(sentence) #see actual http request with header

     if sentence.startswith("GET"):
          path = (sentence.split())[1][1:]
          print(path)
          response = serve_html_file(path)
          #if os.path.exists(path):
          
               






     
     # Send the reply
     connectionSocket.send(response)
     
     # Close connection to client (but not welcoming socket)
     connectionSocket.close()
