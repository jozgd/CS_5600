# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf

pg.init()
import ttt_gui

defaultFont = pg.font.SysFont('Calibri', 28)
msgFont = pg.font.SysFont('Calibri', 22)
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
        self.textBox = pg.Rect(50, 516, 924, 42)
        self.tbActive = False
        self.tbColor = tbInactiveColor
        self.userText = ''

        # make chatbox (to hold displayed chat messages) and chatbox accessories
        # todo: make window scrollable
        self.chatBox = pg.Rect(50, 50, 924, 451)
        self.cbColor = pg.color.Color((255,255,255))

        self.title = defaultFont.render('User '+str(otherID), True, (25,25,25))
        self.titleBox = self.title.get_rect(center=(512, 25))

        self.back = defaultFont.render('Back', True, (25,25,25))
        self.backBox = self.back.get_rect(center=(15+(self.back.get_width()/2), 25))


    def printChatMessages(self):
        # set initial pos values for first message
        bubbleXrecv = self.chatBox.x+5
        bubbleY = self.chatBox.y+5
        # print all chat messages
        for msg in self.convo.msgList:
            if msg.type == 'game':
                game = msg.data
                bubble = None
                chatText = None
                # other user took their turn
                if msg.sender == self.otherID:
                    # it's currently the client user's turn
                    if game.active and game.currentTurn == self.clientID and not game.moveCompleted:
                        chatText = msgFont.render('It\'s your turn against user {}!'.format(self.otherID), True, (225, 225, 225))
                        bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(self.screen, gameBubbleColor, bubble, border_radius=5)
                        self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                    # client user already took their turn, but game is not over
                    elif game.active and game.moveCompleted:
                        chatText = msgFont.render('User {} played their turn.'.format(self.otherID), True, (25,25,25))
                        bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(self.screen, recvBubbleColor, bubble, border_radius=5)
                        self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                    # if receiving game is inactive, then either that player won or it's a tie
                    elif not game.active:
                        chatText = msgFont.render('Game over - ' + str('user {} won!'.format(self.otherID) if game.winner == self.otherID else 'it\'s a tie!'), True, (25,25,25))
                        bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(self.screen, recvBubbleColor, bubble, border_radius=5)
                        self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                # client user took their turn
                elif msg.sender == self.clientID:
                    # new game - it's client user's turn
                    if game.active and game.currentTurn == self.clientID and not game.moveCompleted:
                        chatText = msgFont.render('It\'s your turn against user {}!'.format(self.otherID), True, msgColor)
                        bubbleXsend = self.chatBox.right-5-chatText.get_width()-10
                        bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(self.screen, gameBubbleColor, bubble, border_radius=5)
                        self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                    elif game.active and game.currentTurn == self.otherID and not game.moveCompleted:
                        pass
                    else:
                        # game is still going
                        if game.active and game.currentTurn == self.clientID and game.moveCompleted:
                            chatText = msgFont.render('You took your turn against user {}.'.format(self.otherID), True, msgColor)
                        # either client user won or it's a tie
                        elif not game.active:
                            chatText = msgFont.render('Game over - ' + str('you won!' if game.winner == self.clientID else 'it\'s a tie!'), True, msgColor)
                        bubbleXsend = self.chatBox.right-5-chatText.get_width()-10
                        bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                         chatText.get_height()+10)
                        pg.draw.rect(self.screen, sendBubbleColor, bubble, border_radius=5)
                        self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                # add to mapping of bubbles/games to check for clicks
                if bubble:
                    self.gameMsgs.append([bubble,game])
            elif msg.type == 'msg':
            # sender's bubble is blue on the right
                if msg.sender == self.clientID:
                    chatText = msgFont.render(msg.data, True, msgColor)
                    bubbleXsend = self.chatBox.right-5-chatText.get_width()-10
                    bubble = pg.Rect(bubbleXsend, bubbleY, chatText.get_width()+10,
                                     chatText.get_height()+10)
                    pg.draw.rect(self.screen, sendBubbleColor, bubble, border_radius=5)
                    self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
                # receiver's bubble is gray on the left
                else:
                    chatText = msgFont.render(msg.data, True, (25,25,25))
                    bubble = pg.Rect(bubbleXrecv, bubbleY, chatText.get_width()+10,
                                     chatText.get_height()+10)
                    pg.draw.rect(self.screen, recvBubbleColor, bubble, border_radius=5)
                    self.screen.blit(chatText, (bubble.x+5, bubble.y+5))
            if chatText:
                bubbleY += chatText.get_height()+15


    def runWindow(self):
        # clock tick object for fps
        clock = pg.time.Clock()

        while True:
            # declares max framerate, keeps app alive
            clock.tick(60)
            for e in pg.event.get():
                # quit the app
                if e.type == QUIT:
                    return False
                if e.type == MOUSEBUTTONDOWN:
                    if self.backBox.collidepoint(e.pos):
                        return True
                    # check if game message was clicked, and display game if so
                    for msg in self.gameMsgs:
                        if msg[0].collidepoint(e.pos):
                            return msg[1]
                    self.tbActive = True if self.textBox.collidepoint(e.pos) else False
                if self.tbActive:
                    if e.type == KEYDOWN:
                        if e.key == K_RETURN:
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
            self.screen.blit(self.title, self.titleBox)
            self.screen.blit(self.back, self.backBox)
            # draw chat window and chat bubbles
            pg.draw.rect(self.screen, self.cbColor, self.chatBox)
            self.convo = chf.getConvo(self.clientID, self.otherID).data
            if not self.convo:
                # print('heck')
                self.convo = hf.chatConvo(self.clientID, self.otherID)
            self.printChatMessages()
            # finally, update the screen
            pg.display.flip()


def main(screen, clientID, otherID):
    pg.init()
    cw = chatWindow(screen, clientID, otherID)
    goback = cw.runWindow()
    return goback

if __name__ == "__main__":
    main()
