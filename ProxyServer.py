from socket import *

host = "localhost"
serverPort = 8080 
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverRoot = "."

serverSocket.listen(1)
print(f"Proxy Server listening on {host}:{serverPort}")


def handle_client_request(client_socket: socket.socket):
    request = client_socket.recv(1024).decode()
    print(f"Received request:\n{request}")

    # Here you would parse the request and forward it to the appropriate server
    # For now, we'll just send a dummy response
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello from Proxy Server</h1>"
    client_socket.send(response)
    client_socket.close()

