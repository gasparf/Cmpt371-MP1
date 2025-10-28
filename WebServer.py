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
     if len(file_name) > 1 :
          try:
               with open(file_path, 'rb') as f:
                    content = f.read()
               headers = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
               return headers + content
          except FileNotFoundError:
               error_content = b"<h1>404 Not Found</h1><p>This is Yan Ting and we cannot find the requested file.</p>"
               headers = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
               return headers + error_content
     else:
         return b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"







while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()


     #404
     print(sentence) #see actual http request with header

     if sentence.startswith("GET"):
          path = (sentence.split())[1][1:]
          html_version = (sentence.split())[2]
          print(html_version)
          if(html_version == "HTTP/1.1" or html_version == "HTTP/1.0"):
              response = serve_html_file(path)
          else: #505
              response = b"HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/html\r\n\r\n" + b"<h1>505 HTTP Version Not Supported</h1><p>This is Yan Ting and we don't recognize the http format.</p>"

          
               






     
     # Send the reply
     connectionSocket.send(response)
     
     # Close connection to client (but not welcoming socket)
     connectionSocket.close()
