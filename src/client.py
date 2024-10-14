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


def create_request(requestType):
    if requestType == 1:  # Send a register request to the server
        return dict()
    elif requestType == 2 or requestType == 5:  # Send a deregister request to the server/Exit the client.
        return dict()
    elif requestType == 3:  # Send a request to see all peer nodes in the system
        return dict()
    elif requestType == 4:  # Send an invite to another client to the server
        return dict()
    

def on_request_recieved(request):
    pass


def get_user_input():
    print("1. Register to the server")
    print("2. Deregister from the server")
    print("3. List other players")
    print("4. Invite a player")
    print("5. Exit")
    user_input = input("Enter a number to select an option: ")
    return user_input

def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    clientSocket = connect_to_server(host, port)
    clientIsConnected = True
    print(f"[Client] successfully connected to Server") #'{socket.gethostbyaddr(host)[1][0]}'!\n")

    try:
        while clientIsConnected:  # while the client is connected to the server
            message = create_request(get_user_input())
            receiveMessage = clientSocket.recv(1024).decode()
            clientSocket.send(message.encode())
            # on recieving a response from the server call the on_request_recieved function
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsConnected = False
        clientSocket.close()

if __name__ == "__main__":
    main() 