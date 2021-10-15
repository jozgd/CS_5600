# Gabrielle

import socket

class tictactoe:
    # I assume we'd want to have separate instances of each active game
    #     stored on the server
    # p1 and p2 should be the usernames of the people playing (strings or ints)
    def __init__(self, p1, p2):
        self.active = True
        self.board = [['   ', '   ', '   '],
                      ['   ', '   ', '   '],
                      ['   ', '   ', '   ']]
        self.players = (p1,p2)
        # p1 will be X and p2 will be O by default
        self.symbols = ('X','O')
        self.currentTurn = p1
        self.winner = None

    def printBoard(self):
        print('|'.join(self.board[0]))
        print('-'*11)
        print('|'.join(self.board[1]))
        print('-'*11)
        print('|'.join(self.board[2]))
        print()

    def updateBoard(self, player, row, col):
        if row not in [0,1,2] or col not in [0,1,2]:
            return False
        if self.board[row][col] != '   ':
            return False
        else:
            symbol = 'X' if player == players[0] else 'O'
            self.board[row][col] = ' ' + symbol + ' '
            return True

    def allSpacesFilled(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '   ':
                    # no winner yet
                    return False
        # tied game
        return True

    def checkWinner(self):
        # check horizontally
        for i in range(3):
            if self.board[i][0] != '   ' and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == ' X ':
                    return self.players[0]
                else:
                    return self.players[1]
        # check vertically
        for i in range(3):
            if self.board[0][i] != '   ' and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] == ' X ':
                    return self.players[0]
                else:
                    return self.players[1]
        # check diagonally
        if self.board[0][0] != '   ' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == ' X ':
                return self.players[0]
            else:
                return self.players[1]
        if self.board[0][2] != '   ' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == ' X ':
                return self.players[0]
            else:
                return self.players[1]
        # no winner yet
        return None

    def updateServer(self):
        # TODO: implement socket stuff once the server is capable of storing
        #     game data
        pass

    def playTurn(self, player):
        if not self.active:
            print('This game has already ended. The winner was {}.'.format(self.winner))
            return

        print('It\'s your turn, user {}!\n'.format(player))
        self.printBoard()
        row = input('Enter a row number (0,1,2): ')
        col = input('Enter a column number (0,1,2): ')
        valid = True
        try:
            row = int(row)
            col = int(col)
        except:
            valid = False
        if valid:
            valid = self.updateBoard(player, row, col)
        while not valid:
            print('Invalid input.')
            row = input('Enter a row number (0,1,2): ')
            col = input('Enter a column number (0,1,2): ')
            valid = True
            try:
                row = int(row)
                col = int(col)
            except:
                valid = False
            if valid:
                valid = self.updateBoard(player, row, col)
        print('\nMove completed!\n')
        self.currentTurn = (players[1] if self.currentTurn == players[0] else players[0])
        # TODO: send update message to server

        self.winner = self.checkWinner()
        if self.winner:
            self.active = False
            self.printBoard()
            print('{} is the winner!'.format(self.winner))
            # TODO: send final update message to server indicating game is over
        elif self.allSpacesFilled():
            self.winner = 'nobody'
            self.active = False
            self.printBoard()
            print('It\'s a tie!')
            # TODO: send final update message to server indicating game is over

# testing
if __name__ == "__main__":
    players = ['p1', 'p2']
    game = tictactoe(players[0], players[1])
    while not game.winner:
        game.playTurn(game.currentTurn)
