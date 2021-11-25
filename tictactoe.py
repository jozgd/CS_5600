# Gabrielle

class tictactoe:
    # I assume we'd want to have separate instances of each active game
    #     stored on the server
    # p1 and p2 should be the usernames of the people playing (strings or ints)
    def __init__(self, p1, p2, id=1):
        global game_id
        self.id = id
        self.active = True
        self.board = [['   ', '   ', '   '],
                      ['   ', '   ', '   '],
                      ['   ', '   ', '   ']]
        self.players = (p1,p2)
        # p1 will be X and p2 will be O by default
        # self.symbols = ('X','O')
        self.currentTurn = p1
        self.moveCompleted = False
        self.winner = None

    # for CLI only
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
            symbol = 'X' if player == self.players[0] else 'O'
            self.board[row][col] = ' ' + symbol + ' '
            self.moveCompleted = True
            return True

    def allSpacesFilled(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '   ':
                    # no winner yet
                    return False
        # tied game
        return True

    def swapTurn(self):
        self.currentTurn = (self.players[1] if self.currentTurn == self.players[0] else self.players[0])

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

    # for GUI only
    def checkGameEnded(self):
        self.winner = self.checkWinner()
        if self.winner:
            self.active = False
            # self.printBoard()
            # print('{} is the winner!'.format(self.winner))
            return True
        elif self.allSpacesFilled():
            self.winner = 'nobody'
            self.active = False
            # self.printBoard()
            # print('It\'s a tie!')
            return True
        return False


    # returns True if the game is still running, False if the game has ended
    # for CLI only
    def playTurn(self, player):
        if not self.active:
            print('This game has ended. The winner was {}.'.format(self.winner))
            return False
        if player != self.currentTurn:
            print("It\'s not your turn!")
            print('It\'s currently {}\'s turn. You are {}.'.format(self.currentTurn, player)) # debug
            return False
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
        self.currentTurn = (self.players[1] if self.currentTurn == self.players[0] else self.players[0])

        self.winner = self.checkWinner()
        if self.winner:
            self.active = False
            self.printBoard()
            print('{} is the winner!'.format(self.winner))
            return False
        elif self.allSpacesFilled():
            self.winner = 'nobody'
            self.active = False
            self.printBoard()
            print('It\'s a tie!')
            return False

        return True

# testing
if __name__ == "__main__":
    players = ['p1', 'p2']
    game = tictactoe(players[0], players[1])
    gameRunning = True
    while gameRunning:
        gameRunning = game.playTurn(game.currentTurn)
