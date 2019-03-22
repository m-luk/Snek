# Project: Snek
#
# Created by Michal Lukaszewicz (remoteVoyager) at 2019-03-22
# mlukaszewicz2@gmail.com

#interface script
import pygame
from config import *
from random import randint


def format_text(msg, font, text_size, text_color):
    new_font = pygame.font.Font(font, text_size)
    new_text = new_font.render(msg, 0, text_color)

    return new_text

class menu:
    """menu template"""

    def __init__(self, font = None, title = None, list_items = None):
        self.font = font
        self.title = title
        self.list_items = list_items




