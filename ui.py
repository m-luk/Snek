# Project: Snek
#
# Created by Michal Lukaszewicz (remoteVoyager) at 2019-03-22
# mlukaszewicz2@gmail.com

# interface script
import pygame
from config import *
from random import randint


def format_text(msg, font, text_size, text_color):
    new_font = pygame.font.Font(font, text_size)
    new_text = new_font.render(msg, 0, text_color)

    return new_text


class Menu:
    """menu template"""

    def __init__(self, screen, title=None, el_list=None, font=DEF_FONT, title_size=M_TITLE_SIZE, el_size=M_EL_SIZE,
                 colors=(MENU_TITLE_COLOR, MENU_INACTIVE_COLOR, MENU_ACTIVE_COLOR), title_spacing=TITLE_SPACING,
                 el_spacing=EL_SPACING, default_option=0):

        """
        :param colors:
            [0] - title color
            [1] - menu item inactive color
            [2] - menu item active color
        """

        assert title_size <= WINDOWHEIGHT, "Title text to large to be rendered"
        assert (el_size * len(el_list) + el_spacing * (len(el_list) - 1) + title_size + title_spacing) < WINDOWHEIGHT, \
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

    def show(self):
        """setups and displays menu"""

        el_from_top_spacing = self.title_spacing + self.title_size + TITLE_SPACING

        # TODO: centralise elements vertically

        # setup coordinates
        #   title
        title_cord = (WINDOWWIDTH / 2 - self.title_rect[2] / 2, self.title_spacing)

        #   elements
        el_cords = [(WINDOWWIDTH / 2 - self.el_rects[i][2] / 2,
                     el_from_top_spacing + i * (self.el_rects[i][3] + self.el_spacing)) for i
                    in range(len(self.el_list_f))]

        # setup texts
        #   title
        self.title_f = format_text(self.title, self.font, self.title_size, self.colors[0])

        #   elements
        self.el_list_f = [format_text(el, self.font, self.el_size, self.colors[1]) for el in self.el_list]  # inactive
        self.el_list_f[self.option] = format_text(self.el_list[self.option], self.font, self.el_size,
                                                  self.colors[2])  # active

        # render
        #   title
        self.screen.blit(self.title_f, title_cord)

        #   elements
        for el_id in range(len(self.el_list)):
            self.screen.blit(self.el_list_f[el_id], el_cords[el_id])

    def run(self):
        """Menu item choosing mechanism"""

        # option boundaries
        min_option = 0
        max_option = len(self.el_list) - 1

        self.screen.fill(BLACK)

        for event in pygame.event.get():
            # quitting
            if event.type == pygame.QUIT:
                return -1

            # menu movement
            elif event.type == pygame.KEYDOWN:
                # move vertically
                if event.key == pygame.K_UP:
                    if self.option > min_option:
                        self.option -= 1
                elif event.key == pygame.K_DOWN:
                    if self.option < max_option:
                        self.option += 1
                elif event.key == pygame.K_RETURN:
                    return self.option

        self.show()

        CLOCK.tick(MENU_FPS)

        return None


class ScoreDisplay:

    def __init__(self, screen, snek, placement="top_right", font=S_D_FONT, font_size=S_D_TEXT_SIZE, color=S_D_COLOR):
        """
        :param placement:
            top_right
            top_left
            low_right
            low_left
        """
        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.color = color
        self.snek = snek
        self.placement = placement

    def change_color(self, color):
        self.color = color

    def change_placement(self, placement):
        self.placement = placement

    def show(self):
        # get snek lenght
        points = len(self.snek) - SNEK_START_SIZE

        points_text = format_text(str(points), self.font, self.font_size, self.color)

        points_text_rect = points_text.get_rect()

        points_cord = [0, 0]

        # set coordinates
        if self.placement == "top_right":
            points_cord = [WINDOWWIDTH - points_text_rect[2], 0]
        elif self.placement == "top_left":
            points_cord = [0, 0]
        elif self.placement == "low_right":
            points_cord = [WINDOWWIDTH - points_text_rect[2], WINDOWHEIGHT - points_text_rect[3]]
        elif self.placement == "low_left":
            points_cord = [0, WINDOWHEIGHT - points_text_rect[3]]

        self.screen.blit(points_text, points_cord)


class ScoreBoard:
    #TODO: scoreboard class
    #TODO: preprare tests for scoreboard
    def __init__(self, screen, scores,  title = "Scoreboard", font = DEF_FONT, title_size = S_B_TITLE_SIZE,
                 score_size = S_B_SCORE_SIZE, title_spacing = 30, score_spacing = 10):
        """scores format: [player name, score]"""

        self.screen = screen

        self.scores = ["\t".join(score) for score in scores]
        self.score_spacing = score_spacing
        self.score_size = score_size

        self.font = font

        self.color = WHITE

        self.title = title
        self.title_size = title_size
        self.title_spacing = title_spacing

        # formatted texts
        self.scores_f = [format_text(el, self.font, self.score_size, WHITE) for el in self.scores]
        self.title_f = format_text(self.title, self.font, self.title_size, self.color)

        # text rectangles
        self.scores_rects = [score.get_rect() for score in self.scores_f]
        self.title_rect = self.title_f.get_rect()

        #scores movement vars
        self.cursor_y = 0
        self.cursor_step = 5

    def __repr__(self):
        for score in self.scores:
            print(str(score))

    def setup(self):

        #title coordinates
        self.title_cord = [(WINDOWWIDTH-self.title_rect[2])/2, self.title_spacing]

        #distance from window border to scores top
        sts = self.title_spacing * 2 + self.title_size

        #scores coordinates
        self.scores_cords = ([[(WINDOWWIDTH - self.scores_rects[i][2]) / 2, sts + i * (self.score_size + self.score_spacing)]
                              for i in range(len(self.scores_rects))])

    def show(self):

        #setup texts
        self.setup()

        #show title
        self.screen.blit(self.title_f, self.title_cord)

        #show scores
        for score_f, score_cord in zip(self.scores_f, self.scores_cords):
            self.screen.blit(score_f, score_cord)

    def run(self):
        """Runs ScoreBoard
            if QUIT or q is pressed returns -1
            if ENTER is pressed returns 0
        """

        self.screen.fill(BLACK)

        self.cursor_y = 0

        #events
        for event in pygame.event.get():
            if event == pygame.QUIT:
                return -1

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    return -1

                elif event.key == pygame.K_RETURN:
                    return 0

                # scores cursor movement
                elif event.key == pygame.K_DOWN:
                    self.cursor_y += self.coursor_step

                elif event.key == pygame.K_UP:
                    self.cursor_y -= self.coursor_step


        self.show()

        CLOCK.tick(MENU_FPS)

        return None

