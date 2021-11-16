# Gabrielle

import pygame
from pygame.locals import *

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def main():
    # start the app
    pygame.init()

    # set screen resolution
    screen = pygame.display.set_mode((1024, 608))
    # set title of window
    pygame.display.set_caption('PyMessage')
    # makes the mouse visible on the screen
    pygame.mouse.set_visible(1)

    # make background
    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((225, 225, 225))

    textBox = pygame.Rect(100, 100, 140, 32)



    # clock tick object for fps
    clock = pygame.time.Clock()

    while True:
        # declares max framerate, keeps app alive
        clock.tick(60)
        for e in pygame.event.get():
            # quit the app
            if e.type == QUIT:
                return
        # draw objects on screen
        screen.blit(bg, (0,0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
