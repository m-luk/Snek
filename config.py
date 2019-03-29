# Project: Snek
#
# Created by Michal Lukaszewicz (remoteVoyager) at 2019-03-22
# mlukaszewicz2@gmail.com

# File storing game configurations
import pygame

# SCREEN
WINDOWWIDTH = 640
WINDOWHEIGHT = 400

# GAMEPLAY
FPS = 15
MENU_FPS=30
MOVEMENT_STEP = 10
SQR_SIZE = 10
SNEK_START_SIZE = 10

# COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

# CLOCK
CLOCK = pygame.time.Clock()

# UI
#   MENUS
TITLE_SPACING = 40
EL_SPACING = 10

#       COLORS
MENU_TITLE_COLOR = WHITE
MENU_ACTIVE_COLOR = RED
MENU_INACTIVE_COLOR = WHITE

#       TEXT
M_TITLE_SIZE = 60
M_EL_SIZE = 30
FONT_1 = "snake_chan.ttf"
DEF_FONT = FONT_1

#   SCORE_DISPLAY
S_D_TEXT_SIZE = 40
S_D_FONT = DEF_FONT
S_D_COLOR = WHITE