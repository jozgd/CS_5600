# Gabrielle

from tictactoe import tictactoe
import pygame as pg
from pygame.locals import *
import time
import copy

testing = True

if testing:
    pg.init()
defaultFont = pg.font.SysFont('Calibri', 28)
gameFont = pg.font.SysFont('Calibri', 56)

class tttGUI:
    def __init__(self, screen, game, player):
        self.screen = screen
        self.game = game                # game is a tictactoe object
        self.player = player            # id of user viewing game

        # make background
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((225, 225, 225))

        # holds rect objects to display game on screen
        self.boardGUI = [[None, None, None],
                         [None, None, None],
                         [None, None, None]]

        self.titleText = 'Tic-tac-toe game between users {} and {}'.format(self.game.players[0], self.game.players[1])

        self.back = defaultFont.render('Back', True, (25,25,25))
        self.backBox = self.back.get_rect(center=(15+(self.back.get_width()/2), 25))

    def updateSquare(self, player, row, col):
        return self.game.updateBoard(player, row, col)

    def drawBoard(self):
        centerX = 512-89
        centerY = 304-89
        for row in range(3):
            for col in range(3):
                newSquare = pg.Rect(centerX-42, centerY-42, 84, 84)
                labelText = '' if self.game.board[row][col] == '   ' else ('X' if self.game.board[row][col] == ' X ' else 'O')
                newLabel = gameFont.render(labelText, True, (25,25,25))
                newLabelBox = newLabel.get_rect(center=newSquare.center)
                pg.draw.rect(self.screen, (200,200,200), newSquare)
                self.screen.blit(newLabel, newLabelBox)
                self.boardGUI[row][col] = (newSquare, newLabel)
                centerX += 89
            centerX = 512-89
            centerY += 89

    def setTitle(self):
        if not self.game.active:
            if self.game.winner == 'nobody':
                self.titleText = 'It\'s a tie!'
            else:
                self.titleText = 'User {} is the winner!'.format(self.game.winner)
        elif self.game.moveCompleted:
            self.titleText = 'Move completed!'
        elif self.player == self.game.currentTurn:
            self.titleText = 'It\'s your turn, user {}!'.format(self.player)
        else:
            self.titleText = 'It\'s not your turn!'

    def runWindow(self):
        # clock tick object for fps
        clock = pg.time.Clock()

        while True:
            # declares max framerate, keeps app alive
            clock.tick(60)
            for e in pg.event.get():
                # quit the app
                if e.type == QUIT:
                    pg.quit()
                if e.type == MOUSEBUTTONDOWN:
                    if self.backBox.collidepoint(e.pos):
                        return True
                    # disable play if not player's turn
                    if self.game.active and self.player == self.game.currentTurn and not self.game.moveCompleted:
                        for row in range(3):
                            for col in range(3):
                                if self.boardGUI[row][col][0].collidepoint(e.pos):
                                    success = self.updateSquare(self.player,row,col)
                                    # if not success:
                                    #     self.titleText = 'Invalid move.'
                                    if success:
                                        # return game object to be sent to server
                                        gameOver = self.game.checkGameEnded()
                                        self.game.moveCompleted = True
                                        gameToReturn = copy.deepcopy(self.game)
                                        gameToReturn.id += 1
                                        gameToReturn.swapTurn()
                                        gameToReturn.moveCompleted = False
                                        return [self.game, gameToReturn]
            self.screen.blit(self.bg, (0,0))
            self.setTitle()
            title = defaultFont.render(self.titleText, True, (25,25,25))
            titleBox = title.get_rect(center=(512, 25))
            self.screen.blit(title, titleBox)
            self.screen.blit(self.back, self.backBox)
            self.drawBoard()
            pg.display.flip()


def test():
    screen = pg.display.set_mode((1024, 608))
    pg.display.set_caption('PyMessage')
    pg.mouse.set_visible(1)
    game = tictactoe(1,2)
    while True:
        gw = tttGUI(screen, game, 1)
        update = gw.runWindow()
        if isinstance(update, tictactoe):
            game = update
        else:
            # print('Game over!')
            return


def main(screen, game, player):
    pg.init()
    gw = tttGUI(screen, game, player)
    return gw.runWindow()


if __name__ == "__main__":
    if testing:
        test()
