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
                 colors=(MENU_TITLE_COLOR, MENU_INACTIVE_COLOR, MENU_ACTIVE_COLOR), title_spacing = TITLE_SPACING, \
                 el_spacing = EL_SPACING, default_option=0):

        """
        :param colors:
            [0] - title color
            [1] - menu item inactive color
            [2] - menu item active color
        """

        assert title_size<=WINDOWHEIGHT, "Title text to large to be rendered"
        assert (el_size * len(el_list) + el_spacing * (len(el_list)-1) + title_size + title_spacing) < WINDOWHEIGHT, \
        "text is too large to render it"

        self.screen = screen

        self.title = title
        self.el_list = el_list

        self.title_f = format_text(title, font, title_size, colors[0])
        self.el_list_f = [format_text(el, font, el_size, colors[1]) for el in self.el_list]

        self.title_size = title_size
        self.el_size = el_size

        self.title_spacing = title_spacing
        self.el_spacing = el_spacing

        self.title_rect = self.title_f.get_rect()
        self.el_rects = [el.get_rect() for el in self.el_list_f]

        self.font = font
        self.colors = colors

        self.option = default_option

    def show_menu(self):
        """setups and displays menu"""

        el_from_top_spacing = self.title_spacing + self.title_size + TITLE_SPACING

        #setup coordinates

        #TODO: centralise elements vertically

        #   title
        title_cord = (WINDOWWIDTH / 2 - self.title_rect[2] / 2, self.title_spacing)

        #   elements
        el_cords = [(WINDOWWIDTH / 2 - self.el_rects[i][2] / 2, el_from_top_spacing + i * (self.el_rects[i][3] + self.el_spacing)) for i
                    in range(len(self.el_list_f))]

        #setup texts
        #   title
        self.title_f = format_text(self.title, self.font, self.title_size, self.colors[0])

        #   elements
        self.el_list_f = [format_text(el, self.font, self.el_size, self.colors[1]) for el in self.el_list]              #inactive
        self.el_list_f[self.option] = format_text(self.el_list[self.option],self.font, self.el_size, self.colors[2])    #active

        #render
        #   title
        self.screen.blit(self.title_f, title_cord)

        #   elements
        for el_id in range(len(self.el_list)):
            self.screen.blit(self.el_list_f[el_id], el_cords[el_id])


    def menu_run(self):
        """Menu item choosing mechanism"""

        #option boundaries
        min_option = 0
        max_option = len(self.el_list)-1

        self.screen.fill(BLACK)

        for event in pygame.event.get():
            #quitting
            if event.type == pygame.QUIT:
                return -1

            #menu movement
            elif event.type == pygame.KEYDOWN:
                #move vertically
                if event.key == pygame.K_UP:
                    if self.option > min_option:
                        self.option -= 1
                elif event.key == pygame.K_DOWN:
                    if self.option < max_option:
                        self.option += 1
                elif event.key == pygame.K_RETURN:
                    return self.option


        self.show_menu()

        CLOCK.tick(MENU_FPS)

        return None


class score_display:

    def __init__(self,screen, snek, placement="top_right", font=S_D_FONT, font_size = S_D_TEXT_SIZE, color = S_D_COLOR):

        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.color = color
        self.snek = snek
        self.placement = placement

    def show_sd(self):

        points = len(self.snek)-SNEK_START_SIZE

        points_text = format_text(str(points), self.font, self.font_size, self.color)

        points_text_rect = points_text.get_rect()

        points_cord = [0,0]

        if self.placement == "top_right":
            points_cord = [WINDOWWIDTH-points_text_rect[2], 0]

        self.screen.blit(points_text, points_cord)









