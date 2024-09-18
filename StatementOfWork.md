# Project Title
Tic-Tac-Toe Game

# Team
Joe M, Erin T, Juan C

# Project Objective
To make the most fun online tic tac toe game. We aim to do this by using TCP communications in Python to have clients compete against each other.

# Scope
## Inclusions:
- Multiplayer
- User/Player Profile
- Application/Transport layer format

## Exclusions:
- None at this time

# Delieverables: 
- server.py
- client.py
- game.py
- startServer.sh
- startClient.sh

# Timeline: 
## Sprint 0 - Setup (Complete by 09/22/24)
- Create the project Github
- Decide on the game
- Create README and SOW

## Sprint 1 - Implement TCP Server/Client (09/22/24 - 10/06/24)
- Set up server side applications
- Set up client side connection
- Establish basic communication between the server and client
- Handle common errors for network related issues
- Test the abilities of the server and client and debug if needed
- Update the README file

## Sprint 2 - Design and Implement Message Protocol (10/06/24 - 10/20/24)
- Define the format of the messages in the exchange
- Handle ways to receive, send, and parse messages with both the server and client
- Handle how the server will deal with client connections and disconnections

## Sprint 3 - Multiplayer functionality: Synchronizing state accross clients (10/20/24 - 11/03/24)
- Synchronize the game state across all connected clients
- Client side game rendering
- Decide and implement how the players will take turns playing the game
- Implement player identification
- Optional: having chat functionality so players can talk to each other

## Sprint 4 - Gameplay (11/03/24 - 11/17/24)
- Update game state management
- Handle user input
- Define winning conditions and implement a notification to players when a winner is determined
- Determine and implement what happens after the game is finished
- Develop a user-friendly UI

## Sprint 5 - Error Handling and Testing (11/17/24 - 12/06/24)
- Handle unexpected errors
- Integration testings
- Security and risk evaluation

# Technical Requirements: 
## Hardware
- Access to a laptop or desktop.
- Access to an internet connection.

## Software
- Python version 3.9 or greater.
- Libraries used will be: sockets
- Any OS

# Assumptions: 
- Everyone who has access to the code has read the README and has access to the materials to run the program.

# Roles and Responsibilities:
## Juan
- Develop and test code

## Erin
- Develop and test code
  
## Joe
- Develop and test code

# Communication Plan:
- Communicate via SMS and Teams

# Additional Notes: 
n/a
