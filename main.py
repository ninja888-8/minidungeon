import pygame
from settings import *
from sprites import *

# runs the actual game instance
class Game:
    # state is either main menu, level selection, in game, or credits screen
    def __init__(self, state):
        self.screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.state = state
        self.type = 0
        self.menu = Menu()
        self.tutorial = Tutorial()
        self.select = Select()
        self.credits = Credits()
        pygame.display.set_caption("mini dungeon!")

    # generates dungeon layout
    def new_dungeon(self, stage):
        self.level = Level(self.type, stage)
        self.level.generate_rooms()

    # program loop
    def run(self):
        while self.state != -1:
            if self.state == 0:
                self.menu_events()
                self.draw_menu()
            elif self.state == 1:
                self.tutorial_events()
                self.draw_tutorial()
            elif self.state == 2:
                self.select_events()
                self.draw_select()
            elif self.state == 3:
                self.playing_events()
                self.draw_playing()
            elif self.state == 4:
                self.credits_events()
                self.draw_credits()
    
    # draws the menu
    def draw_menu(self):
        self.screen.fill(BG)
        self.menu.draw_bg(self.screen)
        pygame.display.flip()

    # draws the tutorial
    def draw_tutorial(self):
        self.screen.fill(BG)
        self.tutorial.draw_bg(self.screen)
        pygame.display.flip()
    
    # draws the game select screen
    def draw_select(self):
        self.screen.fill(BG)
        self.select.draw_bg(self.screen)
        pygame.display.flip()

    # draws the actual game screens
    def draw_playing(self):
        self.screen.fill(BG)
        self.level.draw_bg(self.screen)
        pygame.display.flip()

    # draws the credits screen
    def draw_credits(self):
        self.screen.fill(BG)
        self.credits.draw_bg(self.screen)
        pygame.display.flip()

    # deals with user events in the main menu
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            
            # moving around in menu, cycles around
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu.option += 1
                    self.menu.option %= 4

                if event.key == pygame.K_UP:
                    self.menu.option += 3
                    self.menu.option %= 4

                if event.key == pygame.K_RETURN:
                    if self.menu.option == 0:
                        self.state = 1
                    elif self.menu.option == 1:
                        self.state = 2
                    elif self.menu.option == 2:
                        self.state = 4
                    elif self.menu.option == 3:
                        pygame.quit()
                        quit(0)

    # deals with user events in the tutorial
    def tutorial_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

    # deals with user events in the game selection screen
    def select_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            
            # moving around in menu, cycles around
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.select.option += 1
                    self.select.option %= 3
                
                if event.key == pygame.K_UP:
                    self.select.option += 2
                    self.select.option %= 3

                if event.key == pygame.K_RETURN:
                    if self.select.option == 0:
                        self.type = 0
                        self.state = 3
                        self.new_dungeon(0)
                    elif self.select.option == 1:
                        self.type = 1
                        self.state = 3
                        self.new_dungeon(0)
                    elif self.select.option == 2:
                        self.state = 0

    # deals with user events in the game
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.level.moveU = True
                
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.level.moveD = True

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.level.moveL = True

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.level.moveR = True
                
                if self.level.map[self.level.roomx][self.level.roomy] == 1 and self.level.can_move_next_stage and event.key == pygame.K_RETURN:
                    self.level.next_stage()

                if (self.level.map[self.level.roomx][self.level.roomy] == 3 and event.key == pygame.K_RETURN):
                    self.level.loot_select()

                if event.key == pygame.K_RETURN and self.level.can_move_next_room() != -1 and self.level.can_move:
                    self.level.can_move = False
                    self.level.next_room()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.level.moveU = False
                
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.level.moveD = False

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.level.moveL = False

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.level.moveR = False

                if event.key == pygame.K_RETURN:
                    self.level.can_move = True

            if (self.level.map[self.level.roomx][self.level.roomy] == 4 or self.level.map[self.level.roomx][self.level.roomy] == 1) and event.type == pygame.MOUSEBUTTONDOWN:
                self.level.attack()

    # deals with user events in the credits screen
    def credits_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    quit()


pygame.init()
game = Game(0)
game.run()