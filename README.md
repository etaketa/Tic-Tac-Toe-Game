# Tic-Tac-Toe-Game

Two clients will connect to a server that conducts a game of Tic Tac Toe using Python and socket programming to implement it. Players will play through a text based command line interface in the terminal window with a tic tac toe board that updates with the new position of their opponent.

**How to play:**
1. **Start the server:** Run the `server.py` script by typing the command: `python3 server.py <port>`
2. **Connect clients:** Run the `client.py` script on two different machines or terminals by typing the command: `python3 client.py <serverIP> <port>`
- Each client gets the option to exit or invite a player
- Once a player is invited from a list of available players, the game will start
3. **Play the game:** Players take turns entering their moves by typing in the coordinates that correspond to the box they want to fill in with their symbol (X or O). The first player to get three in a row in any direction wins!

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Socket Programming in Python](https://realpython.com/python-sockets/)
* Homework 1 - Intro to TCP Sockets
* Homework 2 - Multiple TCP Connections
