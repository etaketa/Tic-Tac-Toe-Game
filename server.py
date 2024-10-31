import sys
import socket
import selectors
import game
import logging

sel = selectors.DefaultSelector()
list_of_clients = []

def start_connections():
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            sock = key.fileobj
            client_connection, address = sock.accept()
            print(f"Successfully connected to: {str(address)}")
            sel.register(client_connection, selectors.EVENT_READ, data="hello")
            client_username = client_connection.recv(1024).decode()
            for client in list_of_clients:
                client_connected_msg = '[Server]: ' + client_username + ' connected to the server!'
                bytes_msg = b'%s' % client_connected_msg.encode()
                client.send(bytes_msg)
            list_of_clients.append(client_connection)
            return client_username

def exit(message, client, username):
    if "Exiting..." in message:
        logging.info(f"server.py - Closing {username}'s connection to the server")
        exit_msg = username + " left the server, cancelling the game"
        print(exit_msg)
        list_of_clients.remove(client)
        client.close()
        list_of_clients[0].send(exit_msg.encode())
        list_of_clients[0].close()
        sys.exit(0)

def play_game(client1_user, client2_user):
    logging.info(f"server.py - Starting game play!")
    client1_played = client1_user + " played: \n"
    client2_played = client2_user + " played: \n"
    query_input = "\nWhat position would you like to place? "
    board = "\n" + game.get_board() + query_input
    list_of_clients[0].send(board.encode())
    while True:
        try:
            client_message1 = list_of_clients[0].recv(1024).decode()
            message = "Received from " + client1_user + ": " + str(client_message1)
            exit(message, list_of_clients[0], client1_user)
            print(message)
            board_move = game.make_move(str(client_message1), 'X')
            new_msg = client1_played + board_move + query_input
            list_of_clients[1].send(new_msg.encode())
            board_move += "\nWaiting for other player's turn..."
            list_of_clients[0].send(board_move.encode())
            client_message2 = list_of_clients[1].recv(1024).decode()
            message = "Received from " + client2_user + ": " + str(client_message2)
            exit(message, list_of_clients[1], client2_user)
            print(message)

            board_move = game.make_move(str(client_message2), 'O')
            new_msg = client2_played + board_move + query_input
            list_of_clients[0].send(new_msg.encode())
            board_move += "\nWaiting for other player's turn..."
            list_of_clients[1].send(board_move.encode())
        except BrokenPipeError:
            logging.info(f"server.py - Both clients disconnected from the server")
            print("Both clients disconnected from the server, shutting down the server")
            sys.exit(0)
        except KeyboardInterrupt:
            logging.info(f"server.py - Keyboard interrupt, server is shutting down")
            print("Server is shutting down.")
        finally:
            sel.close()

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
    serverSocket.setblocking(False)
    print(f"[Server] is running and listening on {(host, portNumber)}")
    logging.info(f"server.py - Server is up and runnning")
    sel.register(serverSocket, selectors.EVENT_READ, data=None)

    try:
        while True:
            client1_user = start_connections()
            client2_user = start_connections()
            if len(list_of_clients) == 2:
                logging.info(f"server.py - Both clients connected to the server")
                break
        play_game(client1_user, client2_user)
    except KeyboardInterrupt:
        logging.info(f"server.py - Keyboard interrupt, server is shutting down")
        print("Server is shutting down.")
    finally:
        sel.close()

if __name__ == "__main__":
    main()