# Gabrielle

import pygame as pg
from pygame.locals import *
import client as c
import util.helper_functions as hf
import util.client_helper_fns as chf
from tictactoe import tictactoe

pg.init()
import login
import chatwindow
import convos
import ttt_gui as ttt

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
            if not isinstance(goback, tictactoe):
                otherID = convos.main(screen, clientID)
                if not otherID[0]:
                    return
                otherID = otherID[1]
                goback = chatwindow.main(screen, clientID, otherID)
            if isinstance(goback, tictactoe):
                game = goback
                gameUpdate = ttt.main(screen, game, clientID)
                if isinstance(gameUpdate, list) and isinstance(gameUpdate[0], tictactoe) and isinstance(gameUpdate[1], tictactoe):
                    gameMsg = hf.chatMessage('game', clientID, otherID, gameUpdate[0])
                    chf.sendMsg(clientID, otherID, gameMsg)
                    if gameUpdate[0].active:
                        gameMsg = hf.chatMessage('game', clientID, otherID, gameUpdate[1])
                        chf.sendMsg(clientID, otherID, gameMsg)
                elif gameUpdate == True:
                    goback = chatwindow.main(screen, clientID, otherID)
                else:
                    return

if __name__ == "__main__":
    main()
