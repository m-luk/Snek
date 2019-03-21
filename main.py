import pygame
from random import randint

WINDOWWIDTH = 640
WINDOWHEIGHT = 400
FPS = 15
MOVEMENT_STEP = 10
SQR_SIZE = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)

CLOCK = pygame.time.Clock()


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

    def __repr__(self):
        return "square at ({},{})".format(self.x, self.y)


class snek:
    def __init__(self):
        assert (WINDOWHEIGHT % SQR_SIZE == 0 and WINDOWWIDTH % SQR_SIZE == 0)

        # body creation
        self.body = [square(WINDOWWIDTH / 2 - i * SQR_SIZE, WINDOWHEIGHT / 2, SQR_SIZE) for i in range(10)]

        # print([val.get_cord() for val in self.body])

        self.head = self.body[0].get_cord()
        # movement 2d vector
        self.direction = (1, 0)

    def __len__(self):
        return len(self.body)

    def set_direction(self, vec):
        assert (-1 <= vec[0] <= 1 and -1 <= vec[1] <= 1)

        if not vec == tuple([i * (-1) for i in self.direction]):
            self.direction = vec

    def get_direction(self):
        return self.direction

    def update_pos(self):
        """updates snek position, if direction change is provided (as a vector (dx, dy)) it changes the dir"""

        # print(self.body[0].get_cord())
        print(self.body)

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

            else:
                node.set_cord(last_node.last_pos)

            last_node = node  # save position of the last node

    def get_snek(self):
        return self.body

class App:
    def __init__(self):
        self.size = (WINDOWWIDTH, WINDOWHEIGHT)
        self.run = True
        self.screen = None
        self.snek = None

    def on_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        self.run = True
        self.food_is = False
        self.snek = snek()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.run = False

    def on_loop(self):
        self.screen.fill((0, 0, 0))

        # print(self.p1.get_cord())
        # mechanics
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.snek.set_direction((0, -1))
        if pressed[pygame.K_DOWN]: self.snek.set_direction((0, 1))
        if pressed[pygame.K_LEFT]: self.snek.set_direction((-1, 0))
        if pressed[pygame.K_RIGHT]: self.snek.set_direction((1, 0))

        self.snek.update_pos()

        for node in self.snek.get_snek():
            pygame.draw.rect(self.screen, WHITE, node.gett())

        CLOCK.tick(FPS)

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_run(self):
        if self.on_start() == False:
            self.run = False

        # runloop
        while self.run:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    a1 = App()
    a1.on_run()
