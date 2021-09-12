import pygame
import os


def load_image(name, colorkey=pygame.Color('brown')):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    return image


def alpha_image(image, colorkey=pygame.Color('brown')):
    image.set_colorkey(colorkey)
    return image


def crossing(pos, mousepos, full=False):
    x1, y1 = mousepos
    x2, y2, w2, h2 = pos[0], pos[1], 25, 25
    if full:
        x2, y2, w2, h2 = pos[0], pos[1], pos[2], pos[3]
    if x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2:
        return True
    return False
