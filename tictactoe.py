# Gabrielle

import socket

class tictactoe:
    # I assume we'd want to have separate instances of each active game
    #     stored on the server
    # p1 and p2 should be the usernames of the people playing (strings or ints)
    def __init__(self, p1, p2):
        active = True
        board = [[' ', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        players = {
            p1:'X',
            p2:'O'
        }

    def printBoard(self):
        print('|'.join(self.board[0]))
        print('-'*5)
        print('|'.join(self.board[1]))
        print('-'*5)
        print('|'.join(self.board[2]))

    def updateBoard(self, player, row, col):
        if self.board[row][col] != ' ':
            return False
        else:
            self.board[row][col] = self.players[player]
            return True

    def checkWinner(self):
        # check horizontally
        for i in range(3):
            if self.board[i][0] != ' ' and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return
        # check vertically
        # check diagonally

        return None

    def playTurn(self, player):
        self.printBoard():
