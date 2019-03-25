import pygame
from config import *
from engine import *
from random import randint


class App:
    def __init__(self):
        self.size = (WINDOWWIDTH, WINDOWHEIGHT)
        self.run = True
        self.screen = None
        self.snek = None
        self.new_game = True
        self.font = FONT_1

    def on_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def on_new_game(self):
        self.run = True
        self.snek = snek()
        self.food = food(self.snek)
        self.new_game = False

    def on_event(self, event):
        if event.type == pygame.QUIT:       # for quitting
            self.run = False
        elif event.type == pygame.KEYDOWN:  # keyboard shortcut for quitting
            if event.key == pygame.K_q:
                self.run = False
                return

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
                text_resp = format_text("RESPAWN", self.font, 30, RED)
            else:
                text_resp = format_text("RESPAWN", self.font, 30, WHITE)
            if chs == "quit":
                text_quit = format_text("QUIT", self.font, 30, RED)
            else:
                text_quit = format_text("QUIT", self.font, 30, WHITE)

            resp_square = text_resp.get_rect()
            quit_square = text_quit.get_rect()

            print(resp_square)

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

        if self.snek.if_eats(self.food):
            self.food = food(self.snek)

        for node in self.snek.get_snek():
            pygame.draw.rect(self.screen, node.get_color(), node.gett())

        pygame.draw.rect(self.screen, self.food.get_color(), self.food.gett())


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
    a1.on_start()
    # a1.on_run()

    #temporary debug for UI
    m1 = menu(a1.screen, "Menu1", ["Choice 1", "Choice 2", "Choice 3"])
    while True:
        m1.menu_run()
        a1.on_render()

