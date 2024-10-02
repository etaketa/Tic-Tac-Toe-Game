import sys
import socket
import selectors
import traceback

sel = selectors.DefaultSelector()

if len(sys.argv) != 3:
    print(f"usage ={sys.argv[0]} <portNumber>")
    sys.exit(1)

host = sys.argv[1]
portNumber = int(sys.argv[2])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((host, portNumber))
serverSocket.listen(2) #only allow 2 clients to connect to server
print(f"Server is running and listening on {(host, portNumber)}")
serverIsRunning = True
serverSocket.setblocking(False)
sel.register(serverSocket, selectors.EVENT_READ, data=None)

try:
    events = sel.select(timeout=None)
    key = events[0]
    sock = key[0].fileobj
    client_connection, address = sock.accept()
    print(f"Successfully connected to: {str(address)}")
    
    while True:  # while the server is running
        data = client_connection.recv(1024).decode()

        print(f"Message from client: {str(data)}")
        message = input("Write your message: ")
        client_connection.send(message.encode())

except KeyboardInterrupt:
    print("Exiting")
finally:
    serverIsRunning = False
    client_connection.close()