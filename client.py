import sys
import socket
import selectors
import clientmsg
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
    return clientSocket, address


def create_request(requestType):
    if requestType == 1:  # Send a invite request to the server
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=None, value=requestType),
        )
    elif requestType == 2:
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=None, value=requestType),
        )
    else:
        print("Invalid request type")
        return None

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
    clientSocket, address = connect_to_server(host, port)
    clientIsConnected = True
    print(f"[{socket.gethostname()}] successfully connected to Server")

    try:
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        request = create_request(int(get_user_input()))
        message = clientmsg.Message(sel, clientSocket, address, request)
        sel.modify(clientSocket, events, data=message)
        while True:  # while the client is connected to the server
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    message.close()
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsConnected = False
        clientSocket.close()

if __name__ == "__main__":
    main() 