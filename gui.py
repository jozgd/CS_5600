# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf

pg.init()
import login
import chatwindow
import convos

def main():
    screen = pg.display.set_mode((1024, 608))
    pg.display.set_caption('PyMessage')
    pg.mouse.set_visible(1)

    authSuccess = login.main(screen)
    if not authSuccess[0]:
        # user exited the app (or something else weird happened)
        return
    else:
        # authentication was a success
        clientID = authSuccess[1]
        # otherID = 1 if clientID == 0 else 0
        goback = True
        while goback:
            otherID = convos.main(screen, clientID)
            if not otherID[0]:
                return
            otherID = otherID[1]
            goback = chatwindow.main(screen, clientID, otherID)

if __name__ == "__main__":
    main()
