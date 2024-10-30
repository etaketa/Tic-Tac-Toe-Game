board = [['a', 'b', 'c'],['d', 'e', 'f'],['g', 'h', 'i']]
empty_slots = ['a','b','c','d','e','f','g','h','i']

def get_board():
    printed_board = ""
    for i in range(3):
        for j in range(3):
            printed_board += "|" + board[i][j]
        printed_board += "|\n"
    return printed_board[:len(printed_board) - 1]

def make_move(move, player):
    for i in range(3):
        for j in range(3):
            if board[i][j] == move:
                board[i][j] = player
    return get_board()

def boardFull():
    for i in board:
        for j in board:
            if board[i][j] in empty_slots:
                return False
    return True

def check_for_winner():

    if boardFull():
        return "It's a draw!"
