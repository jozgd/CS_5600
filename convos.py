# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf
from math import log10, floor

defaultFont = pg.font.SysFont('Calibri', 28)
boldFont = pg.font.SysFont('Calibri', 28, bold=True)
tbActiveColor = pg.color.Color('azure2')
tbInactiveColor = pg.color.Color('azure3')
unreadColor = pg.color.Color('royalblue')

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
        self.unreadConvos = []

        # make textbox (for entering ID to make new convo) and textbox accessories
        self.textBox = pg.Rect(50, 516, 924, 42)
        self.tbActive = False
        self.tbColor = tbInactiveColor
        self.userText = ''

        # make convobox (to hold displayed list of conversations) and convobox accessories
        self.convoBox = pg.Rect(50, 50, 924, 451)
        self.cbColor = pg.color.Color((255,255,255))
        self.convoPanel = None
        self.scroll_y = 1.0
        self.offset = 0

        self.title = defaultFont.render('Conversations', True, (25,25,25))
        self.titleBox = self.title.get_rect(center=(512, 25))

    def createConvoList(self):
        panelSize = (924, max(1, len(self.convoList))*43 + 5)
        panelSurface = pg.Surface(panelSize, pg.SRCALPHA)
        bubbleX = 5
        bubbleY = 5
        self.convoButtons = {}
        if self.convoList == []:
            listText = defaultFont.render('No conversations to show.', True, (25,25,25))
            listBox = listText.get_rect(center=(462,bubbleY+21))
            panelSurface.blit(listText, listBox)
        for id in self.convoList:
            self.convoButtons[id] = []
            listText = defaultFont.render('User ' + str(id), True, (25,25,25))
            if id in self.unreadConvos:
                listText = boldFont.render('User ' + str(id), True, (25,25,25))
            listBox = pg.Rect(bubbleX, bubbleY, 914, listText.get_height()+10)
            pg.draw.rect(panelSurface, tbInactiveColor, listBox)
            panelSurface.blit(listText, (listBox.x+5, listBox.y+5))
            if id in self.unreadConvos:
                unreadIndicator = pg.Rect(listText.get_width()+15, listBox.centery-4, 8, 8)
                pg.draw.rect(panelSurface, unreadColor, unreadIndicator, border_radius=4)
            self.convoButtons[id] += [listText, listBox]
            bubbleY += listText.get_height()+15
        self.convoPanel = panelSurface

    def drawConvoList(self, scroll=1.0):
        self.createConvoList()
        dy = self.convoPanel.get_height() - 451
        if dy > 0:
            self.offset = int(dy*scroll)
            tempRect = self.convoPanel.get_rect()
            subRect = pg.Rect(0, self.offset, 924, 451)
            subRectSurface = self.convoPanel.subsurface(subRect)
            surfaceToBlit = subRectSurface
        else:
            surfaceToBlit = self.convoPanel
        return surfaceToBlit

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
                if e.type == MOUSEWHEEL:
                    if e.y == 1:
                        self.scroll_y = max(0, self.scroll_y-0.1)
                        if self.scroll_y != 0.0:
                            self.scroll_y = round(self.scroll_y, -int(floor(log10(abs(self.scroll_y)))))
                    elif e.y == -1:
                        self.scroll_y = min(1, self.scroll_y+0.1)
                        if self.scroll_y != 0.0:
                            self.scroll_y = round(self.scroll_y, -int(floor(log10(abs(self.scroll_y)))))
                    break
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.tbActive = True if self.textBox.collidepoint(e.pos) else False
                    if self.convoBox.collidepoint(e.pos):
                        for id in self.convoList:
                            # this is necessary to calculate where the mouse is *trying* to click...
                            #   the coordinates of each bubble are relative to the subsurface they're
                            #   on whereas the coordinates of the mouse are relative to the screen,
                            #   so it gets weird if you don't calculate the mouse position with
                            #   scrolling and border offsets taken into account
                            mousePos = (e.pos[0]-50, e.pos[1]-50+self.offset)
                            if self.convoButtons[id][1].collidepoint(mousePos):
                                return (True, id)
                if self.tbActive:
                    if e.type == KEYDOWN:
                        if e.key in (K_RETURN, K_KP_ENTER):
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
            unreadMsgs = chf.getUnreadMsgs(self.clientID)
            if unreadMsgs[0]:
                self.unreadConvos = unreadMsgs[1]
            convoPanel = self.drawConvoList(self.scroll_y)
            self.screen.blit(convoPanel, self.convoBox)
            # finally, update the screen
            pg.display.flip()

def main(screen, id):
    pg.init()
    cw = convoWindow(screen, id)
    otherID = cw.runWindow()
    return otherID

if __name__ == "__main__":
    main()
