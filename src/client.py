import sys
import socket
import selectors
import traceback

sel = selectors.DefaultSelector()


def connect_to_server(hostName, portNumber):
    address = (hostName, portNumber)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clientSocket.setblocking(False)
    clientSocket.connect_ex(address)  # connect to the server without blocking the main thread
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(clientSocket, events, data=None)
    return clientSocket



if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
clientSocket = connect_to_server(host, port)
clientIsPlaying = True
print(f"Successfully connected to '{host}'!")
i = 0

try:
    message = input("Write your message: ")
    clientSocket.send(message.encode())
    while True:  # while the client is connected to the server
        receiveMessage = clientSocket.recv(1024).decode()

        print(f"Message from client: {str(receiveMessage)}")
        message = input("Write your message: ")
        clientSocket.send(message.encode())
except KeyboardInterrupt:
    print("Exiting")
finally:
    clientIsPlaying = False
    clientSocket.close()