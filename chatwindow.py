# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf
from tictactoe import tictactoe
from math import log10, floor

defaultFont = pg.font.SysFont('Calibri', 28)
msgFont = pg.font.SysFont('Calibri', 22)
gameMsgFont = pg.font.SysFont('Calibri', 22, italic=True)
msgColor = pg.color.Color('white')
sendBubbleColor = pg.color.Color('royalblue')
recvBubbleColor = pg.color.Color('gray')
gameBubbleColor = pg.color.Color('green2')
tbActiveColor = pg.color.Color('azure2')
tbInactiveColor = pg.color.Color('azure3')

class chatWindow:
    def __init__(self, screen, clientID, otherID):
        # set screen resolution
        self.screen = screen
        self.clientID = clientID
        self.otherID = otherID

        # make background
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((225, 225, 225))

        self.convo = None
        self.gameMsgs = []

        # make textbox and textbox accessories
        self.textBox = pg.Rect(107, 516, 867, 42)
        self.tbActive = False
        self.tbColor = tbInactiveColor
        self.userText = ''

        # make chatbox (to hold displayed chat messages) and chatbox accessories
        self.chatBox = pg.Rect(50, 50, 924, 451)
        self.cbColor = pg.color.Color((255,255,255))
        self.messagePanel = None
        self.scroll_y = 1.0
        self.offset = 0

        self.title = defaultFont.render('User '+str(otherID), True, (25,25,25))
        self.titleBox = self.title.get_rect(center=(512, 25))

        self.back = defaultFont.render('Back', True, (25,25,25))
        self.backBox = self.back.get_rect(center=(15+(self.back.get_width()/2), 25))

        self.unreadIndicator = pg.Rect(self.backBox.topright[0]+3, self.backBox.topright[1]-3, 8, 8)

        self.newGameLabel = defaultFont.render('+', True, (255,255,255))
        self.newGameButton = pg.Rect(50, 516, 42, 42)


    def createMessagePanel(self):
        lenMsgList = 0
        if self.convo:
            for msg in self.convo.msgList:
                if msg.type == 'game':
                    if msg.data.active and msg.data.currentTurn == self.otherID and not msg.data.moveCompleted:
                        pass
                    else:
                        lenMsgList += 1
                else:
                    lenMsgList += 1
        panelSize = (924, lenMsgList*37 + 5)
        panelSurface = pg.Surface(panelSize, pg.SRCALPHA)
        self.gameMsgs = []
        # set initial pos values for first message
        bubbleXrecv = 5
        bubbleY = 5
        # print all chat messages
        if self.convo:
            for msg in self.convo.msgList:
                if msg.type == 'game':
                    game = msg.data
                    bubble = None
                    chatText = None
                    # other user took their turn
                    if msg.sender == self.otherID:
                        # it's currently the client user's turn
                        if game.active and game.currentTurn == self.clientID and not game.moveCompleted:
                            chatText = gameMsgFont.render('It\'s your turn against user {}!'.format(self.otherID), True, msgColor)
                            bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                             chatText.get_height()+10)
                            self.gameMsgs.append([pg.draw.rect(panelSurface, gameBubbleColor, bubble, border_radius=5), game])
                            panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                        # client user already took their turn, but game is not over
                        elif game.active and game.moveCompleted:
                            chatText = gameMsgFont.render('User {} played their turn.'.format(self.otherID), True, (25,25,25))
                            bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                             chatText.get_height()+10)
                            self.gameMsgs.append([pg.draw.rect(panelSurface, recvBubbleColor, bubble, border_radius=5), game])
                            panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                        # if receiving game is inactive, then either that player won or it's a tie
                        elif not game.active:
                            chatText = gameMsgFont.render('Game over - ' + str('user {} won!'.format(self.otherID) if game.winner == self.otherID else 'it\'s a tie!'), True, (25,25,25))
                            bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                             chatText.get_height()+10)
                            self.gameMsgs.append([pg.draw.rect(panelSurface, recvBubbleColor, bubble, border_radius=5), game])
                            panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                    # client user took their turn
                    elif msg.sender == self.clientID:
                        # new game - it's client user's turn
                        if game.active and game.currentTurn == self.clientID and not game.moveCompleted:
                            chatText = gameMsgFont.render('It\'s your turn against user {}!'.format(self.otherID), True, msgColor)
                            bubbleXsend = 924-5-(chatText.get_width()+10)
                            bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                             chatText.get_height()+10)
                            self.gameMsgs.append([pg.draw.rect(panelSurface, gameBubbleColor, bubble, border_radius=5), game])
                            panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                        elif game.active and game.currentTurn == self.otherID and not game.moveCompleted:
                            pass
                        else:
                            # game is still going
                            if game.active and game.currentTurn == self.clientID and game.moveCompleted:
                                chatText = gameMsgFont.render('You took your turn against user {}.'.format(self.otherID), True, msgColor)
                            # either client user won or it's a tie
                            elif not game.active:
                                chatText = gameMsgFont.render('Game over - ' + str('you won!' if game.winner == self.clientID else 'it\'s a tie!'), True, msgColor)
                            bubbleXsend = 924-5-(chatText.get_width()+10)
                            bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                             chatText.get_height()+10)
                            self.gameMsgs.append([pg.draw.rect(panelSurface, sendBubbleColor, bubble, border_radius=5), game])
                            panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                    # add to mapping of bubbles/games to check for clicks
                    # if bubble:
                    #     self.gameMsgs.append([bubble,game])
                elif msg.type == 'msg':
                # sender's bubble is blue on the right
                    if msg.sender == self.clientID:
                        chatText = msgFont.render(msg.data, True, msgColor)
                        bubbleXsend = 924-5-(chatText.get_width()+10)
                        bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(panelSurface, sendBubbleColor, bubble, border_radius=5)
                        panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                    # receiver's bubble is gray on the left
                    else:
                        chatText = msgFont.render(msg.data, True, (25,25,25))
                        bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(panelSurface, recvBubbleColor, bubble, border_radius=5)
                        panelSurface.blit(chatText, (bubble.x+5, bubble.y+5))
                if chatText:
                    bubbleY += chatText.get_height()+15
        self.messagePanel = panelSurface

    def drawMessagePanel(self, scroll=1.0):
        self.createMessagePanel()
        dy = self.messagePanel.get_height() - 451
        if dy > 0:
            self.offset = int(dy*scroll)
            tempRect = self.messagePanel.get_rect()
            subRect = pg.Rect(0, self.offset, 924, 451)
            subRectSurface = self.messagePanel.subsurface(subRect)
            surfaceToBlit = subRectSurface
        else:
            surfaceToBlit = self.messagePanel
        return surfaceToBlit

    def runWindow(self):
        # clock tick object for fps
        clock = pg.time.Clock()

        while True:
            # declares max framerate, keeps app alive
            clock.tick(60)

            # set color of textbox based on whether it's active
            tbColor = tbActiveColor if self.tbActive else tbInactiveColor
            # place objects on screen
            self.screen.blit(self.bg, (0,0))
            # draw textbox and surface for input text to show
            pg.draw.rect(self.screen, tbColor, self.textBox)
            if not self.tbActive and self.userText == '':
                textSurface = defaultFont.render('Type a new message here and press ENTER to send', True, (255,255,255))
            else:
                textSurface = defaultFont.render(self.userText, True, (25,25,25))
            textSurfaceBox = textSurface.get_rect(center=(self.textBox.x+5+(textSurface.get_width()/2), self.textBox.centery))
            self.screen.blit(textSurface, textSurfaceBox)
            # draw button to create new game
            pg.draw.rect(self.screen, sendBubbleColor, self.newGameButton)
            newGameBox = self.newGameLabel.get_rect(center=(71,537))
            self.screen.blit(self.newGameLabel, newGameBox)
            # draw title and back button
            self.screen.blit(self.title, self.titleBox)
            self.screen.blit(self.back, self.backBox)
            # draw chat window and chat bubbles
            pg.draw.rect(self.screen, self.cbColor, self.chatBox)
            self.convo = chf.getConvo(self.clientID, self.otherID).data
            if not self.convo:
                self.convo = hf.chatConvo(self.clientID, self.otherID)
            msgPanel = self.drawMessagePanel(self.scroll_y)
            self.screen.blit(msgPanel, self.chatBox)
            unreadMsgs = chf.getUnreadMsgs(self.clientID)
            if unreadMsgs[0]:
                pg.draw.rect(self.screen, sendBubbleColor, self.unreadIndicator, border_radius=4)

            for e in pg.event.get():
                # quit the app
                if e.type == QUIT:
                    return False
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
                # e.button = 1 means that the left mouse button was clicked
                elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if self.backBox.collidepoint(e.pos):
                        return True
                    # check if game message was clicked, and display game if so
                    elif self.chatBox.collidepoint(e.pos):
                        for msg in self.gameMsgs:
                            # this is necessary to calculate where the mouse is *trying* to click...
                            #   the coordinates of each bubble are relative to the subsurface they're
                            #   on whereas the coordinates of the mouse are relative to the screen,
                            #   so it gets weird if you don't calculate the mouse position with
                            #   scrolling and border offsets taken into account
                            mousePos = (e.pos[0]-50, e.pos[1]-50+self.offset)
                            if msg[0].collidepoint(mousePos):
                                return msg[1]
                    elif self.newGameButton.collidepoint(e.pos):
                        nextGameID = chf.getNextGameID()
                        newGame = tictactoe(self.clientID, self.otherID, nextGameID)
                        newMsg = hf.chatMessage('game', self.clientID, self.otherID, newGame)
                        chf.sendMsg(self.clientID, self.otherID, newMsg)
                        return newGame
                    self.tbActive = True if self.textBox.collidepoint(e.pos) else False
                if self.tbActive:
                    if e.type == KEYDOWN:
                        if e.key in (K_RETURN, K_KP_ENTER):
                            if self.userText != '':
                                newMsg = hf.chatMessage('msg', self.clientID, self.otherID, self.userText)
                                chf.sendMsg(self.clientID, self.otherID, newMsg)
                                self.userText = ''
                        elif e.key == K_BACKSPACE:
                            self.userText = self.userText[:-1]
                        else:
                            tsTemp = defaultFont.render(self.userText+e.unicode, True, (0,0,0))
                            if tsTemp.get_width() > self.textBox.w-10:
                                pass
                            else:
                                self.userText += e.unicode

            # finally, update the screen
            pg.display.flip()


def main(screen, clientID, otherID):
    pg.init()
    cw = chatWindow(screen, clientID, otherID)
    goback = cw.runWindow()
    return goback

if __name__ == "__main__":
    main()
