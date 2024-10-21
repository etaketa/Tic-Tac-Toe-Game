import sys
import socket
import selectors
import logging
import threading
import clientmsg

sel = selectors.DefaultSelector()


def create_request(requestType):
    logging.info(f"client.py - Creating request type {requestType}")
    print(f"Creating request type {requestType}")

    if requestType == 1:  # Send an invite request to the server
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
    logging.info("client.py - Getting user input")
    print("1. Invite a player")  # maybe list all players and ask for the player to invite
    print("2. Exit")
    user_input = input("Enter a number to select an option: ")
    return user_input


# This is a function handled in a seperate thread
def handle_server_communication(clientSocket):
    try:
        while True:
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
        logging.info("Caught keyboard interrupt, disconnecting from the server")
        print("Disconnecting from the server")
    finally:
        logging.info("Closing connection to the server and closing client socket")
        clientSocket.close()


# This is a function handled in a seperate thread
def handle_user_input(clientSocket, address):
    while True:
        user_input = get_user_input()
        request = create_request(int(user_input))

        if request:
            message = clientmsg.Message(sel, clientSocket, address, request)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            sel.modify(clientSocket, events, data=message)


def connect_to_server(host, port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    clientSocket.setblocking(False)
    sel.register(clientSocket, selectors.EVENT_READ, data=None)
    return clientSocket, clientSocket.getsockname()


def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    clientSocket, address = connect_to_server(host, port)
    logging.info(f"[{socket.gethostname()}] successfully connected to Server")
    print(f"[{socket.gethostname()}] successfully connected to Server")

    # Start threads for server communication and user input
    server_thread = threading.Thread(target=handle_server_communication, args=(clientSocket,))
    user_input_thread = threading.Thread(target=handle_user_input, args=(clientSocket, address))

    server_thread.start()
    user_input_thread.start()

    server_thread.join()
    user_input_thread.join()

if __name__ == "__main__":
    main()