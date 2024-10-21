import sys
import socket
import selectors
import traceback
import servermsg
import logging

sel = selectors.DefaultSelector()
dict_of_clients = {}
list_of_clients = []


def start_connections():
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)


def shutdown_server():
    logging.info("Shutting down server.")
    # TODO: Debug further
    # for client in dict_of_clients.values():
    #     try:
    #         client.close()
    #     except Exception as e:
    #         logging.error(f"Failed to send shutdown message to client: {e}")
    
    sel.close()


def accept_wrapper(sock):
    client_connection, address = sock.accept()
    logging.info(f"Accepted connection from: {address[0]}")
    print(f"Accepted connection from: {address[0]}")
    client_connection.setblocking(False)
    # print(f"Client connection {client_connection}")
    # print(f"Address {address}") 
    dict_of_clients[address] = client_connection
    list_of_clients.append(client_connection)

    if len(dict_of_clients) > 1:
        notify_clients_of_new_connection(address)

    message = servermsg.Message(sel, client_connection, address, dict_of_clients, list_of_clients)
    sel.register(client_connection, selectors.EVENT_READ, data=message)


# General notify clients function that sends a message to all clients
def notify_clients(message, clientBeingAddedOrRemoved=None):
    logging.info("[Server]: Sending notification to all clients")
    print(f"[Server]: Sending notification to all clients")
    other_clients = {addr: conn for addr, conn in dict_of_clients.items() if conn != clientBeingAddedOrRemoved}

    for addr, client in other_clients.items():
        try:
            logging.info(f"[Server] Sending notification to {addr}")
            print(f"[Server] Sending notification to {addr}")
            message_obj = servermsg.Message(sel, client, addr, message, list_of_clients)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            sel.modify(client, events, data=message_obj)
            service_connection(sel.get_key(client), selectors.EVENT_WRITE)
        except Exception as e:
            logging.error(f"Failed to send notification to client: {e}")


# Sends a notification to all clients that a new client has joined the server
def notify_clients_of_new_connection(new_client_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(new_client_address[0])
    except socket.herror:
        hostname = new_client_address[0]  # If hostname lookup fails, use the IP address

    notification_message = {
        "type": "text/json",
        "encoding": "utf-8",
        "content": {
            "action": "join",
            "value": f"{hostname} has joined the server."
        }
    }

    notify_clients(notification_message, clientBeingAddedOrRemoved=dict_of_clients[new_client_address])


# Sends a notification to all clients if a client has disconnected from the server
def notify_clients_of_disconnection(disconnected_client_address):
    
    try:
        hostname, _, _ = socket.gethostbyaddr(disconnected_client_address[0])
    except socket.herror:
        hostname = disconnected_client_address[0]  # If hostname lookup fails, use the IP address

    notification_message = {
        "type": "text/json",
        "encoding": "utf-8",
        "content": {
            "action": "disconnect",
            "value": f"{hostname} has left the server."
        }
    }

    
    notify_clients(notification_message)
    # list_of_clients.remove(disconnected_client_address)


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