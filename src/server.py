import sys
import socket
import selectors
import traceback

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
    sel.register(client_connection, selectors.EVENT_READ, data="hello")
    list_of_clients.append(client_connection)

def service_connection(key, mask):
    sock = key.fileobj
    if mask & selectors.EVENT_READ:
        data = sock.recv(1024)  # Adjust buffer size as needed
        if data:
            handle_request(data, sock)
        else:
            sel.unregister(sock)
            sock.close()

def invite_player():
    host_names = "Pick a letter from the list of host names:\n"
    counter = 97
    for client in list_of_clients:
        client = str(client)
        host_names += chr(counter) + ". " + socket.gethostbyaddr(client[110:123])[1][0] + "\n"
        counter += 1
    response = host_names[:len(host_names) - 1]
    return b"%s" % response.encode()

def handle_request(request=None, sock=None):
    requestType = int.from_bytes(request, "big")
    if requestType == 1:
        response = invite_player()
        print("Sending response to client...")
        sock.send(response)
    elif requestType == 2:
        print("Disconnecting client from server...")
        response = b"Exit"
        sock.send(response)
        sel.unregister(sock)
        sock.close()
    else:
        print("Not an available option")
    # unpack the request
    # check the value of the request
    # send the appropriate response
    # print("Sending response to client...")
    # sock.send(response)

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