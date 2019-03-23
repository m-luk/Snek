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

    def __init__(self, screen, title = None, el_list = None, font = DEF_FONT, title_size=M_TITLE_SIZE, el_size = M_EL_SIZE, \
                 colors=None, title_spacing = TITLE_SPACING, el_spacing = EL_SPACING):

        assert title_size>= WINDOWHEIGHT, "Title text to large to be rendered"
        assert (el_size * len(el_list) + el_spacing * (len(el_list)-1) + title_size + title_spacing) > WINDOWHEIGHT, \
        "text is too large to render it"

        self.screen = screen

        self.title = format_text(font, title, title_size, title, colors[0])
        self.el_list = [format_text(font, el, el_size, colors[1]) for el in el_list ]

        self.title_size = title_size
        self.el_size = el_size

        self.title_spacing = title_spacing
        self.el_spacing = el_spacing

        self.title_rect = self.title.get_rect()
        self.el_rects = [el.get_rect() for el in self.el_list]

        self.font = font

        self.title_color = colors[0]
        self.el_colors = [colors[1] for el in el_list]

    def show_menu(self):
        """displays menu"""

        el_from_top_spacing = self.title_spacing + self.title_size + TITLE_SPACING

        #setup coordinates
        #   title
        title_cord = (WINDOWWIDTH / 2 - self.title_rect[2] / 2, self.title_spacing)

        #   elements
        el_cords = [(WINDOWWIDTH / 2 - self.el_rects[i][2] / 2, el_from_top_spacing + i * (self.el_rects[i][3] + self.el_spacing)) for i
                    in range(len(self.el_list))]

        #render
        #   title
        self.screen.blit(self.title, title_cord)

        #   elements
        for el_id in len(self.el_list):
            self.screen.blit(self.el_list[el_id], el_cords[el_id])

    def menu_run(self):
        run = True

        option = 0

        #options:
        # [0] - start new game
        # [1] - check leaderboard
        # [2] - credits
        # [3] - quit







