import sys
import socket
import selectors
import traceback

sel = selectors.DefaultSelector()

def start_connections():
    events = sel.select(timeout=None)
    key = events[0]
    sock = key[0].fileobj
    client_connection, address = sock.accept()
    print(f"Successfully connected to: {str(address)}")
    return client_connection


def main():
    if len(sys.argv) != 2:
        print(f"usage = {sys.argv[0]} <portNumber>")
        sys.exit(1)

    host = socket.gethostname()
    portNumber = int(sys.argv[1])

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host, portNumber))
    serverSocket.listen(2) #only allow 2 clients to connect to server
    print(f"[Server] is running and listening on {(host, portNumber)}")
    serverIsRunning = True
    serverSocket.setblocking(False)
    sel.register(serverSocket, selectors.EVENT_READ, data=None)

    connected_clients = [] # list of all the connected clients

    try:
        while serverIsRunning:  # while the server is running
            connected_clients.append(start_connections())
        # client_connection1 = start_connections()
        # message = "Waiting for another client..."
        # client_connection1.send(message.encode())
        # client_connection2 = start_connections()

        # message = "Both clients are connected!"
        # client_connection1.send(message.encode())

        

            # client_message1 = client_connection1.recv(1024).decode()
            # message = "Received from client 1: " + str(client_message1)
            
            # client_connection2.send(message.encode())
            # client_message2 = client_connection2.recv(1024).decode()
            # message = "Received from client 2: " + str(client_message2)
            # client_connection1.send(message.encode())

    except KeyboardInterrupt:
        serverIsRunning = False
        print("Exiting")
    finally:
        for client in connected_clients:
            client.close()

        serverSocket.close()

if __name__ == "__main__":
    main()