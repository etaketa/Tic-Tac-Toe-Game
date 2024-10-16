import sys
import socket
import selectors
import traceback
import json

sel = selectors.DefaultSelector()


def connect_to_server(hostName, portNumber):
    address = (hostName, portNumber)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setblocking(False)
    clientSocket.connect_ex(address)  # connect to the server without blocking the main thread
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(clientSocket, events, data=None)
    return clientSocket


def create_request(requestType):
    if requestType == 1:  # Send a invite request to the server
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(1)
        )
    elif requestType == 2:
        # deregister from the server
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(2)
        )
    else:
        print("Invalid request type")
        return None
    

def handle_response(response, clientSocket):
    # unpack response
    # if repsonse is deregister value, close socket
    # else handle other responses
    pass



def get_user_input():
    # print("2. Deregister from the server")
    # print("3. List other players")
    print("1. Invite a player") # maybe list all players and ask for the player to invite
    print("2. Exit")
    user_input = input("Enter a number to select an option: ")
    return user_input

def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    clientSocket = connect_to_server(host, port)
    clientIsConnected = True
    print(f"[{socket.gethostname()}] successfully connected to Server") #'{socket.gethostbyaddr(host)[1][0]}'!\n")

    try:
        while clientIsConnected:  # while the client is connected to the server
            # get the user input
            message = create_request(int(get_user_input()))
            # clientSocket.send(json.dumps(message).encode()) # find a way to correctly send the message to the server
            # handle_response(clientSocket.recv(1024), clientSocket)
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsConnected = False
        clientSocket.close()

if __name__ == "__main__":
    main() 