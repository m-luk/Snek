import pygame
from random import randint

WINDOWWIDTH = 640
WINDOWHEIGHT = 400
FPS = 15
MOVEMENT_STEP = 10
SQR_SIZE = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)

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

        self.head_cord = self.body[0].get_cord()
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

    def get_snek(self):
        return self.body

    def update_pos(self):
        """updates snek position, if direction change is provided (as a vector (dx, dy)) it changes the dir"""

        # print(self.body[0].get_cord())
        #print(self.body)

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


class App:
    def __init__(self):
        self.size = (WINDOWWIDTH, WINDOWHEIGHT)
        self.run = True
        self.screen = None
        self.snek = None
        self.new_game = True
        self.font = "snake_chan.ttf"

    def on_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def on_new_game(self):
        self.run = True
        self.food_is = False
        self.snek = snek()
        self.new_game = False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.run = False
                return

    def format_text(self, msg, font, text_size, text_color):
        new_font = pygame.font.Font(font, text_size)
        new_text = new_font.render(msg, 0, text_color)

        return new_text

    def on_crash(self):
        """handles crashesh with obstacles and canibalism"""

        self.screen.fill(BLACK)

        menu = True
        chs = "respawn"

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        chs = "respawn"
                    elif event.key == pygame.K_DOWN:
                        chs = "quit"
                    elif event.key == pygame.K_RETURN:
                        if chs == "respawn":
                            self.new_game = True
                            return
                        elif chs == "quit":
                            self.run=False
                            return

            self.screen.fill(BLACK)

            if chs == "respawn":
                text_resp = self.format_text("RESPAWN", self.font, 30, RED)
            else:
                text_resp = self.format_text("RESPAWN", self.font, 30, WHITE)
            if chs == "quit":
                text_quit = self.format_text("QUIT", self.font, 30, RED)
            else:
                text_quit = self.format_text("QUIT", self.font, 30, WHITE)

            resp_square = text_resp.get_rect()
            quit_square = text_quit.get_rect()

            self.screen.blit(text_resp, (WINDOWWIDTH/2-resp_square[2]/2, 160))
            self.screen.blit(text_quit, (WINDOWWIDTH/2-quit_square[2]/2, 190))

            pygame.display.update()
            CLOCK.tick(FPS)

    def on_loop(self):
        self.screen.fill(BLACK)

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

            if self.new_game:
                self.on_new_game()

            self.on_loop()
            if self.snek.is_canibal():
                self.on_crash()

            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    a1 = App()
    a1.on_run()

