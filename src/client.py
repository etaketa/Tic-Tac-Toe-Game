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


def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    clientSocket = connect_to_server(host, port)
    clientIsPlaying = True
    print(f"Successfully connected to '{socket.gethostbyaddr(host)[1][0]}'!\n")

    # TODO: this is where we should send a RegisterRequest from this Client to the server so the server can know things such as the client socket

    try:
        while clientIsPlaying:  # while the client is connected to the server
            # TODO: While the client is connected to the user, they could ask to see a list of other nodes in the system, invite a particular node, and play a game, or leave the server
            receiveMessage = clientSocket.recv(1024).decode()
            if receiveMessage == "Waiting for another client...":
                print(str(receiveMessage))
                print()
            else:
                print(str(receiveMessage))
                message = input("Write your message: ")
                clientSocket.send(message.encode())
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsPlaying = False
        clientSocket.close()

if __name__ == "__main__":
    main()