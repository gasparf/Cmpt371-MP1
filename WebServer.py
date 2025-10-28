from socket import *
import os
from datetime import datetime, timezone
from email.utils import format_datetime, parsedate_to_datetime

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverRoot = "."

serverSocket.listen(1)
print ('The server is ready to receive')

# insert HTTP responses for code 304, 403

# used for 304 code to check when last modified
def _http_date_from_ts(ts: float) -> str:
     # Format epoch timestamp to RFC 7231 IMF-fixdate (e.g., 'Sun, 06 Nov 1994 08:49:37 GMT').
     return format_datetime(datetime.fromtimestamp(ts, timezone.utc), usegmt=True)

# check isforbidden for 403 seperately to be called in serve_html_file
def _is_forbidden(requested_path: str) -> bool:
     # Normalize and resolve path under serverRoot
     abs_root = os.path.abspath(serverRoot)
     abs_target = os.path.abspath(os.path.join(serverRoot, requested_path))

     # Block path traversal outside of root
     if not abs_target.startswith(abs_root + os.sep) and abs_target != abs_root:
          return True

     # Block access to hidden files/dirs (starting with '.')
     rel = os.path.relpath(abs_target, abs_root)
     parts = rel.split(os.sep)
     if any(p.startswith('.') and p not in ('.', '..') for p in parts):
          return True

     # If file exists but is not readable, forbid
     if os.path.exists(abs_target) and not os.access(abs_target, os.R_OK):
          return True

     return False





#404 and 200
def serve_html_file(file_name, request_headers=None):
     """Serve a file with basic 200/404 handling and conditional 304 if applicable."""
     file_path = os.path.join(serverRoot, file_name)
     if len(file_name) > 1:
          # 403 Forbidden checks
          if _is_forbidden(file_name):
               error_content = b"<h1>403 Forbidden</h1><p>Access to this resource is denied.</p>"
               headers = (
                    b"HTTP/1.1 403 Forbidden\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Content-Length: " + str(len(error_content)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n"
               )
               return headers + error_content

          try:
               # If-Modified-Since -> 304 Not Modified
               if request_headers and 'if-modified-since' in request_headers:
                    try:
                         ims_dt = parsedate_to_datetime(request_headers['if-modified-since'])
                         if ims_dt.tzinfo is None:
                              ims_dt = ims_dt.replace(tzinfo=timezone.utc)
                    except Exception:
                         ims_dt = None

                    if os.path.isfile(file_path):
                         # Round to whole seconds to avoid sub-second timing diff vs header precision
                         mtime_sec = int(os.path.getmtime(file_path))
                         last_mod_dt = datetime.fromtimestamp(mtime_sec, timezone.utc)
                         if ims_dt is not None and last_mod_dt <= ims_dt:
                              headers = (
                                   b"HTTP/1.1 304 Not Modified\r\n"
                                   b"Date: " + _http_date_from_ts(datetime.now(timezone.utc).timestamp()).encode() + b"\r\n"
                                   b"Last-Modified: " + _http_date_from_ts(mtime_sec).encode() + b"\r\n"
                                   b"Connection: close\r\n\r\n"
                              )
                              return headers  # no body for 304

               with open(file_path, 'rb') as f:
                    content = f.read()
               # Round to whole seconds to align with HTTP-date precision
               mtime_sec = int(os.path.getmtime(file_path))
               headers = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Last-Modified: " + _http_date_from_ts(mtime_sec).encode() + b"\r\n"
                    b"Content-Length: " + str(len(content)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n"
               )
               return headers + content
          except FileNotFoundError:
               error_content = b"<h1>404 Not Found</h1><p>This is Yan Ting and we cannot find the requested file.</p>"
               headers = (
                    b"HTTP/1.1 404 Not Found\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Content-Length: " + str(len(error_content)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n"
               )
               return headers + error_content
          except PermissionError:
               error_content = b"<h1>403 Forbidden</h1><p>Insufficient permissions to read the resource.</p>"
               headers = (
                    b"HTTP/1.1 403 Forbidden\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Content-Length: " + str(len(error_content)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n"
               )
               return headers + error_content
     else:
          # Root request: minimal 200 OK
          return b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"







while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()


     #404
     print(sentence) #see actual http request with header

     if sentence.startswith("GET"):
          # Parse request line and headers
          lines = sentence.split("\r\n")
          try:
               request_line = lines[0]
               method, target, html_version = request_line.split()
          except ValueError:
               response = b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
               connectionSocket.send(response)
               connectionSocket.close()
               continue

          # Build headers dict (case-insensitive)
          headers = {}
          for line in lines[1:]:
               if not line:
                    break
               if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

          path = target[1:]
          print(html_version)
          if (html_version == "HTTP/1.1" or html_version == "HTTP/1.0"):
               response = serve_html_file(path, headers)
          else:  # 505
               response = (
                    b"HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
                    + b"<h1>505 HTTP Version Not Supported</h1><p>This is Yan Ting and we don't recognize the http format.</p>"
               )

    


     
     # Send the reply
     connectionSocket.send(response)
     
     # Close connection to client (but not welcoming socket)
     connectionSocket.close()


