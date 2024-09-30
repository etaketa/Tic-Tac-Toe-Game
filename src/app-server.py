import sys
import socket
import selectors

if len(sys.argv) != 2:
    print(f"usage ={sys.argv[0]} <portNumber>")
    sys.exit(1)

host = socket.gethostname()
portNumber = int(sys.argv[1])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind((host, portNumber))
serverSocket.listen()
print(f"Server is running and listen on {(host, portNumber)}")
serverIsRunning = True
serverSocket.setblocking(False)

i = 0
try:
    while serverIsRunning:
        i += 1
except KeyboardInterrupt:
    print("Exiting")
finally:
    serverIsRunning = False
    print(i)