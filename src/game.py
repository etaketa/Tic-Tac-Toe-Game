import random

class game():
    spaces = None  # A list of the spaces the player can update
    gameBoard = None  # A string of the game board
    players = None  # A list of players


    def __init__(self, p1=None, p2=None, playersList=None):
        # TODO: Initialize p1 and p2 as they will be playing the game
        self.spaces = [" " for _ in range(9)]
        
        self.gameBoard = (
        self.spaces[0] + "|" + self.spaces[1] + "|" + self.spaces[2] + "\n"
        "-|-|-\n"
        + self.spaces[3] + "|" + self.spaces[4]+ "|" + self.spaces[5] + "\n"
        "-|-|-\n"
        + self.spaces[6] + "|" + self.spaces[7]+ "|" + self.spaces[8] + "\n"
        )

        # TODO: Get rid of the last new line character?

        self.players = playersList
    

    def drawBoard(self):
        print(self.gameBoard)


    def updateBoard(self):
        self.gameBoard = (
        self.spaces[0] + "|" + self.spaces[1] + "|" + self.spaces[2] + "\n"
        "-|-|-\n"
        + self.spaces[3] + "|" + self.spaces[4]+ "|" + self.spaces[5] + "\n"
        "-|-|-\n"
        + self.spaces[6] + "|" + self.spaces[7]+ "|" + self.spaces[8] + "\n"
        )

    
    def updateSpace(self, index, char):
        self.spaces[index - 1] = char
        self.updateBoard()

    
    def userTurn(self, player=None):
        validInput = False
        print("Where (1-9)?")
        while validInput == False:
            userIn = int(input())

            if userIn >= 1 and userIn <= 9:
                return userIn
            else:
                print("Please pick a number between 1 and 9")


    def getPlayersList(self):
        return self.players


    def decidePlayer(self):
        return random.randint(0, 1)


    def startGame(self):
        gameIsRunning = True

        decidedIndex = self.decidePlayer()
        
        opp = None
        if decidedIndex == 1:
            opp = 0
        else:
            opp = 1
        
        player1 = self.getPlayersList()[decidedIndex] # Decide which player goes first
        player2 = self.getPlayersList()[opp]

        self.askPlayer(player1) # Decide their symbol -> p2 then gets the opposite
        
        while gameIsRunning:  # play the game
            self.drawBoard() # draw the board
            self.updateSpace(self.userTurn(), 't') # take a users turn, update the board
            # check if the user has won
        
        

testGame = game()
print(testGame.decidePlayer())
# testGame.drawBoard()
# testGame.updateSpace(testGame.userTurn(), 'X')
# testGame.drawBoard()
