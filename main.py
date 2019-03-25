import pygame
from config import *
from engine import *
from ui import *
from random import randint


class App:
    def __init__(self):
        self.size = (WINDOWWIDTH, WINDOWHEIGHT)
        self.run = False
        self.screen = None
        self.snek = None
        self.new_game = True
        self.font = FONT_1

    def on_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def on_start_menu(self):
        title = "S N E K"
        menu_elements = ["New Game", "Leaderboard", "Credits", "Quit"]
        self.m1 = menu(self.screen, title, menu_elements)

        main_menu=True

        while main_menu:
            menu_choice = self.m1.menu_run()
            if menu_choice is not None:
                if menu_choice==0:
                    self.run = True
                    main_menu = False
                elif menu_choice==1:
                    #TODO: leaderboard
                    pass
                elif menu_choice==2:
                    #TODO: credits
                    pass
                elif menu_choice ==3:
                    #quit
                    main_menu = False
                    self.run = False
            self.on_render()

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
        """handles crashes with obstacles and cannibalism"""

        m2 = menu(self.screen, "You Died", ["RESPAWN", "QUIT"])

        menu_run = True

        while menu_run:
            choice = m2.menu_run()
            if choice == 0:
                self.new_game = True
                menu_run = False
            elif choice == 1:
                self.run=False
                menu_run = False

            self.on_render()


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

        self.on_start_menu()

        # game runloop
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
    a1.on_run()



