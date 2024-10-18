import sys
import socket
import selectors
import traceback
import json

sel = selectors.DefaultSelector()
clientIsConnected = False

def connect_to_server(hostName, portNumber):
    address = (hostName, portNumber)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clientSocket.setblocking(False)
    clientSocket.connect_ex(address)  # connect to the server without blocking the main thread
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(clientSocket, events, data=None)
    return clientSocket


def create_request(requestType):
    if requestType == 1:  # Send a invite request to the server
        return requestType.to_bytes(1, "big")
    elif requestType == 2:
        return requestType.to_bytes(1, "big")
    else:
        print("Invalid request type")
        return None
    

def handle_response(response, clientSocket):
    # unpack response
    # if repsonse is deregister value, close socket
    # else handle other responses
    if response == "Exit":
        print("Disconnecting from server...")
        clientIsConnected = False
        clientSocket.close()
        sys.exit(1)
    else:
        print(response)


def get_user_input():
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
        message = create_request(int(get_user_input()))
        clientSocket.send(message)
        handle_response(clientSocket.recv(1024).decode(), clientSocket)
        while clientIsConnected:  # while the client is connected to the server
            message = input()
            clientSocket.send(message.encode())
            handle_response(clientSocket.recv(1024).decode(), clientSocket)
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsConnected = False
        clientSocket.close()

if __name__ == "__main__":
    main() 