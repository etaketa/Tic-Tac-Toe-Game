import sys
import socket
import selectors
import traceback
import servermsg

sel = selectors.DefaultSelector()
list_of_clients = []

def start_connections():
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

def accept_wrapper(sock):
    client_connection, address = sock.accept()
    print(f"Successfully connected to: {str(address)}")
    client_connection.setblocking(False)
    list_of_clients.append(client_connection)
    message = servermsg.Message(sel, client_connection, address, list_of_clients)
    sel.register(client_connection, selectors.EVENT_READ, data=message)

def service_connection(key, mask):
    message = key.data
    try:
        message.process_events(mask)
    except Exception:
        print(
            "server error: exception for",
            f"{message.addr}:\n{traceback.format_exc()}",
        )
        message.close()

def main():
    if len(sys.argv) != 2:
        print(f"usage = {sys.argv[0]} <portNumber>")
        sys.exit(1)

    host = socket.gethostname()
    portNumber = int(sys.argv[1])

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host, portNumber))
    serverSocket.listen(2)  # only allow 2 clients to connect to server
    print(f"[Server] is running and listening on {(host, portNumber)}")
    serverSocket.setblocking(False)
    sel.register(serverSocket, selectors.EVENT_READ, data=None)

    try:
        while True:  # while the server is running
            start_connections()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        sel.close()

if __name__ == "__main__":
    main()