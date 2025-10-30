from socket import *

proxyPort = 8080
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(('', proxyPort))
proxySocket.listen(1)

print(f"Proxy Server listening on port {proxyPort}")

while True:
    # Accept connection from client
    clientSocket, clientAddr = proxySocket.accept()
    print(f"Connection from {clientAddr}")
    
    try:
        # Receive request from client
        request = clientSocket.recv(4096)
        if not request:
            clientSocket.close()
            continue
            
        print(f"Received request:\n{request.decode(errors='replace')}")
        
        # Parse the request line to extract host and port
        lines = request.decode(errors='replace').split("\r\n")
        if not lines:
            clientSocket.close()
            continue
            
        request_line = lines[0]
        parts = request_line.split()
        
        # checks if the request line is valid with at least 2 parts after splitting e.g. GET /test.html
        if len(parts) < 2:
            clientSocket.close()
            continue
        
        # Extract target from request (URL or path)
        target = parts[1]
        
        # Determine target host and port
        # For absolute URLs: http://host:port/path
        # For relative paths: assume localhost:12000 (WebServer)
        # if target.startswith("http://"):
        #     # Parse absolute URL
        #     url_part = target[7:]  # Remove "http://"
        #     if "/" in url_part:
        #         host_port, path = url_part.split("/", 1)
        #         path = "/" + path
        #     else:
        #         host_port = url_part
        #         path = "/"
            
        #     if ":" in host_port:
        #         targetHost, targetPort = host_port.split(":")
        #         targetPort = int(targetPort)
        #     else:
        #         targetHost = host_port
        #         targetPort = 80
        # else:
        
        # Relative path - forward to local WebServer
        targetHost = "localhost"
        targetPort = 12000
        path = target
        
        print(f"Forwarding to {targetHost}:{targetPort}{path}")
        
        # Connect to target server
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((targetHost, targetPort))
        
        # Forward the request to target server
        serverSocket.send(request)
        
        # Receive response from target server
        response = b""
        while True:
            data = serverSocket.recv(4096)
            if not data:
                break
            response += data
            # Simple check: if we received headers and body is complete
            if b"\r\n\r\n" in response:
                # Check if we have Content-Length
                headers_part = response.split(b"\r\n\r\n")[0]
                if b"Content-Length:" in headers_part:
                    # Extract content length and check if body is complete
                    for line in headers_part.split(b"\r\n"):
                        if line.lower().startswith(b"content-length:"):
                            content_length = int(line.split(b":")[1].strip())
                            body_start = response.index(b"\r\n\r\n") + 4
                            if len(response) - body_start >= content_length:
                                break
                # For responses without body or Connection: close
                if b"Connection: close" in headers_part or b"304 Not Modified" in response:
                    break
        
        print(f"Received response ({len(response)} bytes)")
        
        # Send response back to client
        clientSocket.send(response)
        
        # Close connections
        serverSocket.close()
        clientSocket.close()
        
    except Exception as e:
        print(f"Error handling request: {e}")
        clientSocket.close()
    
