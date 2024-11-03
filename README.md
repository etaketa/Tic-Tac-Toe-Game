# Tic-Tac-Toe-Game

Two clients will connect to a server that conducts a game of Tic Tac Toe using Python and socket programming to implement it. Players will play through a text based command line interface in the terminal window with a tic tac toe board that updates with the new position of their opponent.

**How to play:**
1. **Start the server:** Run the `server.py` script by typing the command: `python3 server.py <port>`
2. **Connect clients:** Run the `client.py` script on two different machines or terminals by typing the command: `python3 client.py <serverIP or hostname> <port>`
- Once a player connects to the server, they can input a username
- Once 2 clients are connected and inserted their username, the game will start
3. **Play the game:** Players take turns entering their moves by typing in the coordinates that correspond to the box they want to fill in with their symbol (X or O). The first player to get three in a row in any direction wins!
- The first person to connect will always go first with their symbol being the 'X'
- Choose from the letters a-i to pick where you want your symbol to go
- Board will update with and replace the letter you chose with their symbol

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Socket Programming in Python](https://realpython.com/python-sockets/)
* Homework 1 - Intro to TCP Sockets
* Homework 2 - Multiple TCP Connections

## Sprints
## Sprint 1
Implement a TCP server and TCP client

## Sprint 2 - Design and Implement Message Protocol
Implement a message protocol using libserver.py and custom requests on the client level

## Sprint 3 - Multi-player functionality, Synchronize state across clients.
Add multiplayer functionality
