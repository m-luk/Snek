# Project: Snek
#
# Created by Michal Lukaszewicz (remoteVoyager) at 2019-03-22
# mlukaszewicz2@gmail.com

# File storing game configurations
import pygame


WINDOWWIDTH = 640
WINDOWHEIGHT = 400
FPS = 10
MENU_FPS=30
MOVEMENT_STEP = 10
SQR_SIZE = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0, 255, 0)



CLOCK = pygame.time.Clock()

# UI
#   MENUS
TITLE_SPACING = 30
EL_SPACING = 10

#       COLORS
MENU_ACTIVE_COLOR = RED
MENU_INACTIVE_COLOR = WHITE

#       TEXT
M_TITLE_SIZE = 60
M_EL_SIZE = 30
FONT_1 = "snake_chan.ttf"
DEF_FONT = FONT_1