# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf

defaultFont = pg.font.SysFont('Calibri', 28)
tbActiveColor = pg.color.Color('azure2')
tbInactiveColor = pg.color.Color('azure3')

class convoWindow:
    def __init__(self, screen, id):
        self.screen = screen
        self.clientID = id

        # make background
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((225, 225, 225))

        self.convoList = []
        self.convoButtons = {}

        # make textbox (for entering ID to make new convo) and textbox accessories
        self.textBox = pg.Rect(50, 516, 924, 42)
        self.tbActive = False
        self.tbColor = tbInactiveColor
        self.userText = ''

        # make convobox (to hold displayed list of conversations) and convobox accessories
        self.convoBox = pg.Rect(50, 50, 924, 451)
        self.cbColor = pg.color.Color((255,255,255))

        self.title = defaultFont.render('Conversations', True, (25,25,25))
        self.titleBox = self.title.get_rect(center=(512, 25))

    def printConvoList(self):
        bubbleX = self.convoBox.x+5
        bubbleY = self.convoBox.y+5
        self.convoButtons = {}
        if self.convoList == []:
            listText = defaultFont.render('No conversations to show.', True, (25,25,25))
            listBox = listText.get_rect(center=(512,bubbleY+21))
            self.screen.blit(listText, listBox)
        for id in self.convoList:
            self.convoButtons[id] = []
            listText = defaultFont.render('User ' + str(id), True, (25,25,25))
            listBox = pg.Rect(bubbleX, bubbleY, self.convoBox.right-60, listText.get_height()+10)
            pg.draw.rect(self.screen, tbInactiveColor, listBox)
            self.screen.blit(listText, (listBox.x+5, listBox.y+5))
            self.convoButtons[id] += [listText, listBox]
            bubbleY += listText.get_height()+15

    def runWindow(self):
        # clock tick object for fps
        clock = pg.time.Clock()

        while True:
            # declares max framerate, keeps app alive
            clock.tick(60)
            for e in pg.event.get():
                # quit the app
                if e.type == QUIT:
                    return (False, None)
                if e.type == MOUSEBUTTONDOWN:
                    self.tbActive = True if self.textBox.collidepoint(e.pos) else False
                    for id in self.convoList:
                        for item in self.convoButtons[id]:
                            tempItem = item
                            if isinstance(item, pg.Surface):
                                tempItem = item.get_rect()
                            if tempItem.collidepoint(e.pos):
                                return (True, id)
                if self.tbActive:
                    if e.type == KEYDOWN:
                        if e.key == K_RETURN:
                            valid = False
                            try:
                                otherID = int(self.userText)
                                valid = chf.userExists(otherID)
                            except:
                                pass
                            if not valid:
                                print('Unable to find conversation to open.')
                                self.userText = ''
                                pass
                            else:
                                return (True, otherID)
                        elif e.key == K_BACKSPACE:
                            self.userText = self.userText[:-1]
                        else:
                            tsTemp = defaultFont.render(self.userText+e.unicode, True, (0,0,0))
                            if tsTemp.get_width() > self.textBox.w-10:
                                pass
                            else:
                                self.userText += e.unicode
            # set color of textbox based on whether it's active
            tbColor = tbActiveColor if self.tbActive else tbInactiveColor
            # place objects on screen
            self.screen.blit(self.bg, (0,0))
            # draw textbox and surface for input text to show
            pg.draw.rect(self.screen, tbColor, self.textBox)
            if not self.tbActive and self.userText == '':
                textSurface = defaultFont.render('Enter a user ID and press ENTER to start a new conversation', True, (255,255,255))
            else:
                textSurface = defaultFont.render(self.userText, True, (25,25,25))
            textSurfaceBox = textSurface.get_rect(center=(self.textBox.x+5+(textSurface.get_width()/2), self.textBox.centery))
            self.screen.blit(textSurface, textSurfaceBox)
            self.screen.blit(self.title, self.titleBox)
            # draw conversation list
            pg.draw.rect(self.screen, self.cbColor, self.convoBox)
            self.convoList = chf.getChats(self.clientID)
            self.printConvoList()
            # finally, update the screen
            pg.display.flip()

def main(screen, id):
    pg.init()
    cw = convoWindow(screen, id)
    otherID = cw.runWindow()
    return otherID

if __name__ == "__main__":
    main()
