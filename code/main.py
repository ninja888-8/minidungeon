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
        self.select = Select()
        self.credits = Credits()
        self.achievements = Achievements(False,False)
        pygame.display.set_caption("mini dungeon!")

        self.ending_1 = False
        self.ending_2 = False

    # generates dungeon layout
    def new_dungeon(self, stage):
        self.level = Level(self.type, stage+2)
        self.level.generate_rooms()

    # end of the game screen
    def end_game(self, ending):
        self.state = 4
        self.end = End(self.level.stage, self.level.rooms_explored, self.level.gold_earned, ending)
        self.end.draw_cutscene(self.screen)

        if ending == 1:
            self.ending_1 = True
        elif ending == 2:
            self.ending_2 = True

        self.achievements = Achievements(self.ending_1, self.ending_2)

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
                self.end_events()
                self.draw_end()
            elif self.state == 5:
                self.credits_events()
                self.draw_credits()
            elif self.state == 6:
                self.achievements_events()
                self.draw_achievements()

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

    # draws the end game screen
    def draw_end(self):
        self.screen.fill(BG)
        self.end.draw_bg(self.screen)
        pygame.display.flip()

    # draws the credits screen
    def draw_credits(self):
        self.screen.fill(BG)
        self.credits.draw_bg(self.screen)
        pygame.display.flip()

    # draws the achievemenets screen
    def draw_achievements(self):
        self.screen.fill(BG)
        self.achievements.draw_bg(self.screen)
        pygame.display.flip()

    # deals with user events in the main menu
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # moving around in menu, cycles around
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_D:
                    self.menu.option += 1
                    self.menu.option %= 4

                if event.key in CONTROL_U:
                    self.menu.option += 3
                    self.menu.option %= 4

                if event.key in CONTROL_CONFIRM:
                    if 0 <= self.menu.option <= 3:
                        self.menu.button_animation(self.screen, self.menu.option)

                    if self.menu.option == 0:
                        self.state = 1
                        self.tutorial = Tutorial()
                    elif self.menu.option == 1:
                        self.state = 2
                    elif self.menu.option == 2:
                        self.state = 5
                    elif self.menu.option == 3:
                        pygame.quit()
                        quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and 900 <= pygame.mouse.get_pos()[0] <= 950 and 650 <= pygame.mouse.get_pos()[1] <= 700:
                self.state = 6

    # deals with events that move the player
    def movement_events(self, obj, event):
        match event.type:
            case pygame.KEYDOWN:
                is_pressed = True
            case pygame.KEYUP:
                is_pressed = False
            case _:
                return
        if event.key in CONTROL_U:
            obj.moveU = is_pressed
        if event.key in CONTROL_D:
            obj.moveD = is_pressed
        if event.key in CONTROL_L:
            obj.moveL = is_pressed
        if event.key in CONTROL_R:
            obj.moveR = is_pressed

    # deals with user events in the tutorial
    def tutorial_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            self.movement_events(self.tutorial, event)

            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_CONFIRM and not self.tutorial.generating_message:
                    self.tutorial.generating_message = True
                    self.tutorial.slide += 1
                    if self.tutorial.slide == 10:
                        self.tutorial.roomx = 2
                        self.tutorial.roomy = 3
                        self.tutorial.next_room()
                    elif self.tutorial.slide == 11:
                        self.tutorial.roomx = 3
                        self.tutorial.roomy = 2
                        self.tutorial.next_room()
                    elif self.tutorial.slide == 12:
                        self.tutorial.roomx = 1
                        self.tutorial.roomy = 2
                        self.tutorial.next_room()
                    elif self.tutorial.slide == 13:
                        self.tutorial.roomx = 2
                        self.tutorial.roomy = 1
                        self.tutorial.next_room()
                    elif self.tutorial.slide == 14:
                        self.tutorial.next_stage()
                    elif self.tutorial.slide == 17:
                        self.state = 0

            if event.type == pygame.KEYUP:
                if event.key in CONTROL_CONFIRM:
                    self.tutorial.can_move = True

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() >= self.tutorial.next_attack_time:
                self.tutorial.attack()

    # deals with user events in the game selection screen
    def select_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # moving around in menu, cycles around
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_D:
                    self.select.option += 1
                    self.select.option %= 3
                
                if event.key in CONTROL_U:
                    self.select.option += 2
                    self.select.option %= 3

                if event.key in CONTROL_CONFIRM:
                    if 0 <= self.select.option <= 2:
                        self.select.button_animation(self.screen, self.select.option)

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
        if self.level.lives <= 0:
            self.end_game(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            self.movement_events(self.level, event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key in CONTROL_U:
                    self.level.moveU = True
                
                if event.key == pygame.K_s or event.key in CONTROL_D:
                    self.level.moveD = True

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.level.moveL = True

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.level.moveR = True
                
                if self.level.map[self.level.roomx][self.level.roomy].type == 1 and self.level.map[self.level.roomx][self.level.roomy].cleared and 280 <= self.level.x <= 470 and 280 <= self.level.y <= 470 and not self.level.shopping and event.key in CONTROL_CONFIRM:
                    if self.level.gamemode == 0 and self.level.stage == 2:
                        self.end_game(1)
                    else:
                        self.level.next_stage()


                if self.level.shopping and event.key in CONTROL_CONFIRM:
                    self.level.shop_select()

                if self.level.map[self.level.roomx][self.level.roomy].type == 3 and event.key in CONTROL_CONFIRM:
                    self.level.loot_select()

                if self.level.map[self.level.roomx][self.level.roomy].type == 2 and event.key in CONTROL_CONFIRM:
                    self.level.minigame_select(-1, -1)

                if self.level.map[self.level.roomx][self.level.roomy].type == 2 and self.level.map[self.level.roomx][self.level.roomy].minigame.type == 2 and event.key in CONTROL_D:
                    self.level.map[self.level.roomx][self.level.roomy].minigame.option += 1
                    self.level.map[self.level.roomx][self.level.roomy].minigame.option %= 4

                if self.level.map[self.level.roomx][self.level.roomy].type == 2 and self.level.map[self.level.roomx][self.level.roomy].minigame.type == 2 and event.key in CONTROL_U:
                    self.level.map[self.level.roomx][self.level.roomy].minigame.option += 3
                    self.level.map[self.level.roomx][self.level.roomy].minigame.option %= 4

                if event.key in CONTROL_CONFIRM and 0 <= self.level.can_move_next_room() <= 3:
                    self.level.next_room()
                elif event.key in CONTROL_CONFIRM and self.level.can_move_next_room() == 4:
                    self.end_game(2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key in CONTROL_U:
                    self.level.moveU = False
                
                if event.key == pygame.K_s or event.key in CONTROL_D:
                    self.level.moveD = False

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.level.moveL = False

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.level.moveR = False

                if event.key in CONTROL_CONFIRM:
                    self.level.can_move = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.level.map[self.level.roomx][self.level.roomy].type == 2:
                    self.level.minigame_select(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                elif pygame.time.get_ticks() >= self.level.next_attack_time:
                    self.level.attack()

    # deals with user events in the end game screen
    def end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_CONFIRM:
                    self.state = 0

    # deals with user events in the credits screen
    def credits_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_CONFIRM:
                    self.credits.button_animation(self.screen)
                    self.state = 0

    # deals with user events in the achievements screen
    def achievements_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # moving around in menu, cycles around
            if event.type == pygame.KEYDOWN:
                if event.key in CONTROL_D:
                    self.achievements.option += 1
                    self.achievements.option %= 3
                
                if event.key in CONTROL_U:
                    self.achievements.option += 2
                    self.achievements.option %= 3

                if event.key in CONTROL_CONFIRM:
                    if self.achievements.option == 2:
                        self.achievements.button_animation(self.screen)

                    if self.achievements.option == 2:
                        self.state = 0

pygame.init()
game = Game(0)
game.run()