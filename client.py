import sys
import socket
import selectors
import threading
import logging

sel = selectors.DefaultSelector()
clientIsConnected = False

def connect_to_server(hostName, portNumber):
    address = (hostName, portNumber)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect_ex(address)  # connect to the server without blocking the main thread
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(clientSocket, events, data=None)
    return clientSocket


def create_request(requestType, username):
    if username or dataIsValid(requestType):
        logging.info(f"client.py - Valid request has been made")
        request = requestType
        return b"%s" % request.encode()
    else:
        logging.info(f"client.py - Unexpected request has been made")
        print("Invalid request type")
        return None

def dataIsValid(data):
    valid_input = ['a','b','c','d','e','f','g','h','i']
    for character in valid_input:
        if character == data:
            return True
    return False

def handle_server_communication(clientSocket, address):
    try:
        while True:
            try:
                data = clientSocket.recv(1024)
                if "cancelling" in data.decode():
                    print("Disconnecting from the server")
                    sys.exit(0)
                if data:
                    print(data.decode())
            except Exception as e:
                clientSocket.close()
    except KeyboardInterrupt:
        print("Disconnecting from the server")
        sys.exit(0)
    finally:
        clientSocket.close()

def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    clientSocket = connect_to_server(host, port)
    clientIsConnected = True
    address = 1
    logging.info(f"client.py - {socket.gethostname()} successfully connected to the server")
    print(f"[{socket.gethostname()}] successfully connected to Server")

    user_input_thread = threading.Thread(target=handle_server_communication, args=(clientSocket, address), daemon=True)
    user_input_thread.start()

    try:
        message = create_request(input("Enter desired username: "), True)
        clientSocket.send(message)
        while clientIsConnected:
            message = create_request(input(), False)
            if message:
                clientSocket.send(message)
    except KeyboardInterrupt:
        print("Disconnecting from the server")
    finally:
        clientIsConnected = False
        sys.exit(0)

if __name__ == "__main__":
    main() 