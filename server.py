import sys
import socket
import selectors
import traceback
import servermsg
import logging

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
    logging.info(f"Accepted connection from: {address[0]}")
    print(f"Accepted connection from: {address[0]}")
    client_connection.setblocking(False)
    list_of_clients.append(client_connection)

    if len(list_of_clients) > 1:
        notify_clients_of_new_connection(address, client_connection)

    message = servermsg.Message(sel, client_connection, address, list_of_clients)
    sel.register(client_connection, selectors.EVENT_READ, data=message)


##
# notify_clients_of_new_connection
# @param new_client_address
# @return none
# Sends a notification to all clients that a new client has joined the server
def notify_clients_of_new_connection(new_client_address, new_client_connection):
    response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }

    notification_message = {
        "type": "notification",
        "message": f"New client joined: {new_client_address}"
    }
    other_clients = [client for client in list_of_clients if client != new_client_connection]

    # Notify existing clients about the new connection
    for client in other_clients:
        try:
            client.send(json.dumps(notification_message).encode('utf-8'))
        except Exception as e:
            logging.error(f"Failed to send notification to client: {e}")

            
def service_connection(key, mask):
    message = key.data
    try:
        message.process_events(mask)
    except Exception:
        logging.info(f"server error: exception for {message.addr}:\n{traceback.format_exc()}")
        print(f"server error: exception for {message.addr}:\n{traceback.format_exc()}")
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
    logging.info(f"[Server] is running and listening on {(host, portNumber)}")
    serverSocket.setblocking(False)
    sel.register(serverSocket, selectors.EVENT_READ, data=None)

    try:
        while True:  # while the server is running
            start_connections()
    except KeyboardInterrupt:
        logging.info("Caught Keyboard Interrupt. Server is shutting down.")
        print("Server is shutting down.")
    finally:
        logging.info("Closing server socket.")
        sel.close()

if __name__ == "__main__":
    main()