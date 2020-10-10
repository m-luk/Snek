# Project: Snek
#
# Created by Michal Lukaszewicz (remoteVoyager) at 2019-03-22
# mlukaszewicz2@gmail.com

#Script engine

import pygame
from config import *
from ui import *
from random import randint, randrange

class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_pos = None

    def set_cord(self, cord, save_last=True):
        if save_last:
            self.last_pos = (self.x, self.y)

        self.x = cord[0]
        self.y = cord[1]

    def get_cord(self):
        return [self.x, self.y]

    def get_last_cord(self):
        return self.last_pos

    def move_by_vector(self, vec, multi, save_last=True):
        if save_last:
            self.last_pos = (self.x, self.y)

        self.last_pos = (self.x, self.y)
        self.x += vec[0] * multi
        self.y += vec[1] * multi


class square(position):
    def __init__(self, x, y, a, color=None):
        position.__init__(self, x, y)
        self.a = a
        self.area = a ** 2
        self.color = color

    def gett(self):
        return pygame.Rect(self.x, self.y, self.a, self.a)

    def get_color(self):
        return self.color

    def __repr__(self):
        return "square at ({},{})".format(self.x, self.y)


class food(square):
    def __init__(self, snek: object):
        loop = True

        while loop:
            loop = False
            self.x = randrange(0, WINDOWWIDTH, SQR_SIZE)
            self.y = randrange(0, WINDOWHEIGHT, SQR_SIZE)
            for node in snek.get_snek():
                if node.get_cord() == (self.x, self.y):
                    loop = True
                    break

        square.__init__(self, self.x, self.y, SQR_SIZE, WHITE)


    def __repr__(self):
        return "food at ({},{})".format(self.x, self.y)


class snek:
    def __init__(self):
        assert (WINDOWHEIGHT % SQR_SIZE == 0 and WINDOWWIDTH % SQR_SIZE == 0)

        # body creation
        self.body = [square(WINDOWWIDTH / 2 - i * SQR_SIZE, WINDOWHEIGHT / 2, SQR_SIZE, SNEK_COLOR) for i in range(SNEK_START_SIZE)]

        # print([val.get_cord() for val in self.body])

        self.head_cord = self.body[0].get_cord()    # head position
        self.direction = (1, 0)                     # movement 2d vector

    def __len__(self):
        return len(self.body)

    def set_direction(self, vec):
        assert (-1 <= vec[0] <= 1 and -1 <= vec[1] <= 1)

        #dont allow snake running back and forth
        if not vec == tuple([i * (-1) for i in self.direction]):
            self.direction = vec

    def get_direction(self):
        return self.direction

    def get_snek(self):
        return self.body

    def update_pos(self):
        """updates snek position, if direction change is provided (as a vector (dx, dy)) it changes the dir"""

        # print(self.body[0].get_cord())
        # print(self.body)

        last_node = None

        # change position of all snek nodes
        for node in self.body:
            if node == self.body[0]:
                node.move_by_vector(self.direction, MOVEMENT_STEP)  # move head by vector direction

                # handle snek head out of window bounds
                # x axis
                if node.get_cord()[0] >= WINDOWWIDTH:
                    node.set_cord([0, node.get_cord()[1]], False)
                elif node.get_cord()[0] < 0:
                    node.set_cord([WINDOWWIDTH - SQR_SIZE, node.get_cord()[1]], False)

                # y axis
                if node.get_cord()[1] >= WINDOWHEIGHT:
                    node.set_cord([node.get_cord()[0], 0], False)
                elif node.get_cord()[1] < 0:
                    node.set_cord([node.get_cord()[0], WINDOWHEIGHT-SQR_SIZE], False)

                self.head_cord = node.get_cord()

            else:
                node.set_cord(last_node.last_pos)

            last_node = node  # save position of the last node

    def is_canibal(self):
        """checks if snake is eating himself"""
        for node in self.body[1::]:
            if node.get_cord() == self.head_cord:
                return True

        return False

    def if_eats(self, food):

            if food.get_cord() == self.head_cord:
                pend_node = self.body[-1].get_last_cord()
                self.body.append(square(pend_node[0], pend_node[1], SQR_SIZE, GREEN))

                return True
            else:
                return False

