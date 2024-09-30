import sys
import socket
import selectors


def connect_to_server(hostName, portNumber):
    address = (hostName, portNumber)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setblocking(False)
    clientSocket.connect_ex(address)  # connect to the server without blocking the main thread



if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
connect_to_server(host, port)
clientIsPlaying = True
i = 0

try:
    while clientIsPlaying:
        i += 1
except KeyboardInterrupt:
    print("Exiting")
finally:
    clientIsPlaying = False