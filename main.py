import pygame
from config import *
from engine import *
from ui import *
from random import randint


class App:
    def __init__(self):

        #app params
        self.size = (WINDOWWIDTH, WINDOWHEIGHT)
        self.screen = None
        self.font = FONT_1

        #app objects
        self.snek = None

        #app states
        self.run = True
        self.start_menu = True
        self.new_game = False
        self.crash = False

    def on_start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def on_start_menu(self):
        title = "S N E K"
        menu_elements = ["New Game", "Leaderboard", "Credits", "Quit"]
        self.m1 = menu(self.screen, title, menu_elements)

        while self.start_menu:
            menu_choice = self.m1.menu_run()
            if menu_choice is not None:

                if menu_choice == -1 or menu_choice == 3:   #quit statement
                    self.run = False
                    self.start_menu = False

                if menu_choice==0:      #new game
                    self.run = True
                    self.new_game = True
                    self.start_menu = False

                elif menu_choice==1:    #leaderboard
                    #TODO: leaderboard
                    pass

                elif menu_choice==2:    #credits
                    #TODO: credits
                    pass

            self.on_render()

    def on_new_game(self):
        #states
        self.run = True
        self.new_game = False
        self.crash = False
        self.loop = True

        #objects
        self.snek = snek()
        self.food = food(self.snek)

        #interface
        self.sd1 = score_display(self.screen, self.snek)

    def on_event(self, event):
        if event.type == pygame.QUIT:       # for quitting
            self.run = False
        elif event.type == pygame.KEYDOWN:  # keyboard shortcut for quitting
            if event.key == pygame.K_q:
                self.run = False
                return

    def on_crash(self):
        """handles crashes with obstacles and cannibalism"""

        m2 = menu(self.screen, "You Died", ["RESPAWN", "MAIN MENU", "QUIT"])

        menu_run = True

        while self.crash:
            choice = m2.menu_run()
            if choice == 0:             #respawn
                self.new_game = True
                self.crash= False
            elif choice == 1:           #main menu
                self.start_menu = True
                self.crash= False
            elif choice == 2:           # quit
                self.run=False
                self.crash = False

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

        #draw snek
        for node in self.snek.get_snek():
            pygame.draw.rect(self.screen, node.get_color(), node.gett())

        #draw food
        pygame.draw.rect(self.screen, self.food.get_color(), self.food.gett())

        #if snake crashed
        if self.snek.is_canibal():
            self.loop = False
            self.crash = True

        #show score display
        self.sd1.show_sd()

    def on_render(self):
        CLOCK.tick(FPS)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_run(self):
        if self.on_start() == False:
            self.run = False

        # game runloop
        while self.run:

            for event in pygame.event.get():
                self.on_event(event)

            if self.start_menu:
                self.on_start_menu()

            if self.new_game:
                self.on_new_game()

            if self.loop:
                self.on_loop()

            if self.crash:
                self.on_crash()

            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    a1 = App()
    a1.on_start()
    a1.on_run()



