# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf

defaultFont = pg.font.SysFont('Calibri', 28)
activeColor = pg.color.Color('azure2')
inactiveColor = pg.color.Color('azure3')

class loginWindow:
    def __init__(self, screen):
        # set screen resolution
        self.screen = screen
        # set title of window
        pg.display.set_caption('PyMessage')
        # makes the mouse visible on the screen
        pg.mouse.set_visible(1)

        # make background
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((225, 225, 225))

        # make textbox and textbox accessories
        self.textBox = pg.Rect(50, 516, 924, 42)
        self.tbActive = False
        self.tbColor = inactiveColor
        self.userText = ''

        self.label = defaultFont.render('Enter your user ID below to login.', True, (25,25,25))
        self.verifText = ''

        self.clientID = None

    def checkLogin(self):
        response = False
        try:
            self.clientID = int(self.userText)
            response = chf.userExists(self.clientID)
        except:
            pass
        self.verifText = 'Success!' if response else 'Login unsuccessful - please try again'
        return response

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
                if self.tbActive:
                    if e.type == KEYDOWN:
                        if e.key == K_RETURN:
                            login = self.checkLogin()
                            if login:
                                return (True, self.clientID)
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
            tbColor = activeColor if self.tbActive else inactiveColor
            verifLabel = defaultFont.render(self.verifText, True, (25,25,25))

            # place objects on screen
            self.screen.blit(self.bg, (0,0))
            # draw textbox and surface for input text to show
            pg.draw.rect(self.screen, tbColor, self.textBox)
            if not self.tbActive and self.userText == '':
                textSurface = defaultFont.render('Type your user ID here and press ENTER to log in', True, (255,255,255))
            else:
                textSurface = defaultFont.render(self.userText, True, (25,25,25))
            textSurfaceBox = textSurface.get_rect(center=(self.textBox.x+5+(textSurface.get_width()/2), self.textBox.centery))
            self.screen.blit(textSurface, textSurfaceBox)
            self.screen.blit(self.label, (50, 50))
            self.screen.blit(verifLabel, (50, 80))

            pg.display.flip()

def main(screen):
    pg.init()
    lw = loginWindow(screen)
    success = lw.runWindow()
    return success
    # print(success)

if __name__ == "__main__":
    main()
