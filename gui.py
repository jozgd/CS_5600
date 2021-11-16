# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf

def main():
    # start the app
    pg.init()

    defaultFont = pg.font.SysFont('Calibri', 28)
    msgFont = pg.font.SysFont('Calibri', 22)
    msgColor = pg.color.Color('white')
    bubbleColor = pg.color.Color('royalblue')
    activeColor = pg.color.Color('azure2')
    inactiveColor = pg.color.Color('azure3')

    # set screen resolution
    screen = pg.display.set_mode((1024, 608))
    # set title of window
    pg.display.set_caption('PyMessage')
    # makes the mouse visible on the screen
    pg.mouse.set_visible(1)

    # make background
    bg = pg.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((225, 225, 225))

    # make textbox and textbox accessories
    textBox = pg.Rect(50, 526, 924, 32)
    tbActive = False
    tbColor = inactiveColor
    userText = ''

    # make chatbox (to hold displayed chat messages) and chatbox accessories
    # chatMessages holds a list of chatMessage objects from helper_functions.py,
    #   much like the chatConvo object does
    # todo:
    # - implement chatConvo
    # - make window scrollable
    chatBox = pg.Rect(50, 50, 924, 451)
    cbColor = pg.color.Color((255,255,255))
    chatMessages = []

    # clock tick object for fps
    clock = pg.time.Clock()

    while True:
        # declares max framerate, keeps app alive
        clock.tick(60)
        for e in pg.event.get():
            # quit the app
            if e.type == QUIT:
                return
            if e.type == MOUSEBUTTONDOWN:
                tbActive = True if textBox.collidepoint(e.pos) else False
            if tbActive:
                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        newMsg = hf.chatMessage('msg', 0, 1, userText)
                        chatMessages.append(newMsg)
                        userText = ''
                    elif e.key == K_BACKSPACE:
                        userText = userText[:-1]
                    else:
                        tsTemp = defaultFont.render(userText+e.unicode, True, (0,0,0))
                        if tsTemp.get_width() > textBox.w-10:
                            pass
                        else:
                            userText += e.unicode
        # set color of textbox based on whether it's active
        tbColor = activeColor if tbActive else inactiveColor

        # place objects on screen
        screen.blit(bg, (0,0))
        # draw textbox and surface for input text to show
        pg.draw.rect(screen, tbColor, textBox)
        textSurface = defaultFont.render(userText, True, (25,25,25))
        screen.blit(textSurface, (textBox.x+5, textBox.y+5))
        # draw chat window and chat bubbles
        pg.draw.rect(screen, cbColor, chatBox)
        # set initial pos values for first message
        bubbleX = chatBox.x+5
        bubbleY = chatBox.y+5
        # print all chat messages
        # todo: implement way to create different bubbles depending on whether
        #   message is from client or other user
        for msg in chatMessages:
            chatText = msgFont.render(msg.data, True, msgColor)
            bubble = pg.Rect(bubbleX, bubbleY, chatText.get_width()+10,
                             chatText.get_height()+10)
            pg.draw.rect(screen, bubbleColor, bubble, border_radius=5)
            screen.blit(chatText, (bubble.x+5, bubble.y+5))
            bubbleY += chatText.get_height()+15
        # update max width of textbox if text overflows
        # textBox.w = max(100, textSurface.get_width()+10)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
