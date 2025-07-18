import pygame
import random
from settings import *

# enemies in the game!
class Enemy:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawning = True
        self.spawn_time = pygame.time.get_ticks()
        self.next_move_time = self.spawn_time + 2000
        self.hp = self.max_hp = random.randint(2,2+stage)
        self.stage = stage

        self.x = random.randint(100,650)
        self.y = random.randint(100,650)

    def move(self, person_x, person_y):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_move_time:
            self.next_move_time = cur_time + 10
            if person_x != self.x or person_y != self.y:
                choice = random.randint(0,1)
                if choice == 0 or person_y == self.y:
                    if self.x > person_x:
                        self.x -= 1
                    elif self.x < person_x:
                        self.x += 1
                    elif self.x == person_x:
                        choice = 1
                
                if choice == 1:
                    if self.y > person_y:
                        self.y -= 1
                    elif self.y < person_y:
                        self.y += 1

    def attack(self, person_x, person_y):
        if abs(person_x - self.x) + abs(person_y - self.y) <= (10+self.stage):
            return True
        else:
            return False

    def draw_bg(self, screen):
        screen.blit(enemy_default, (self.x, self.y))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-11, self.y-15, 40, 9))
        pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-9, self.y-13, 36.0*self.hp/self.max_hp, 5))

# boss enemy in the game
class Boss:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawn_time = pygame.time.get_ticks()
        self.next_spawn_time = self.spawn_time + 2000
        self.max_hp = 20+5*stage
        self.hp = 20+5*stage
        self.stage = stage

        self.x = 375
        self.y = 375

    def attack(self, person_x, person_y):
        if abs(person_x - self.x) + abs(person_y - self.y) <= 10:
            return True
        else:
            return False

    def summon(self):
        l = []
        num = random.randint(2,min(5,3+self.stage//5))
        for i in range(num):
            l.append(Enemy(self.stage))
        return l

    def draw_bg(self, screen):
        # temporary sprite, will be much bigger in the future
        screen.blit(enemy_default, (self.x, self.y))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-11, self.y-15, 40, 9))
        pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-9, self.y-13, 36.0*self.hp/self.max_hp, 5))

# loot rooms
class Loot:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.can_choose = True
        self.chosen = -1
        self.success = True
        self.stage = stage

        self.chance_1 = max(50, random.randint(70,100) - self.stage)
        self.chance_2 = max(20, random.randint(50,100) - self.stage)
        self.chance_3 = max(15, random.randint(20,100) - self.stage)

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 32)

    def select(self, person_x, person_y):
        num = random.randint(0,100)
        if not self.can_choose:
            return -1
        elif 180 <= person_x <= 270 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 0
            if num <= self.chance_1:
                return 0
            else:
                self.success = False
                return -1
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 1
            if num <= self.chance_2:
                return 1
            else:
                self.success = False
                return -1
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 2
            if num <= self.chance_3:
                return 2
            else:
                self.success = False
                return -2
        else:
            return -1

    def draw_bg(self, screen, person_x, person_y):
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 350, 50, 50))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(350, 350, 50, 50))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(500, 350, 50, 50))

        if self.chosen != -1:
            if self.success:
                pygame.draw.rect(screen, (100,255,100), pygame.Rect(200+150*self.chosen, 350, 50, 50))
            else:
                pygame.draw.rect(screen, (255,100,100), pygame.Rect(200+150*self.chosen, 350, 50, 50))

        if 180 <= person_x <= 270 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of wealth", True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render(str(self.chance_1) + "% to gain " + str(10+self.stage) + " gold", True, (0,0,0)), (100, 600))
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of power", True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render(str(self.chance_2) + "% to gain 10 atk range", True, (0,0,0)), (100, 600))
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of luck", True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render(str(self.chance_3) + "% to gain " + str(2+self.stage//3) + " atk (otherwise lose " + str(1+self.stage//3) + ")", True, (0,0,0)), (100, 600))

# Main menu screen
class Menu:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.option = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("mini dungeon!", True, (0,0,0)), (300,125))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 250, 600, 100))
        screen.blit(self.my_font.render("tutorial?", True, (0,0,0)), (400, 270))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 370, 600, 100))
        screen.blit(self.my_font.render("play!", True, (0,0,0)), (420, 390))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 490, 600, 100))
        screen.blit(self.my_font.render("credits?", True, (0,0,0)), (400, 510))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 610, 600, 100))
        screen.blit(self.my_font.render("exit?", True, (0,0,0)), (420, 630))

# tutorial screen
class Tutorial:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    #def draw_bg(self, screen):
        

# game select screen
class Select:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.option = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("mini dungeon level select!", True, (0,0,0)), (200,125))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 250, 600, 100))
        screen.blit(self.my_font.render("story mode?", True, (0,0,0)), (410, 270))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 400, 600, 100))
        screen.blit(self.my_font.render("endless mode!", True, (0,0,0)), (410, 420))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (400, 570))

        
# actual game screen
class Level:
    def __init__(self, type, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.type = type
        self.stage = stage                                       # how deep in the dungeon
        self.map = [[0 for i in range(5)] for j in range(5)]     # minimap square colours
        self.adj = [[False for i in range(5)] for j in range(5)] # if this room had been adjacent previously

        self.roomx = 2
        self.roomy = 2

        self.x = 375
        self.y = 375

        self.moveU = False
        self.moveD = False
        self.moveL = False
        self.moveR = False

        self.can_move_next_stage = False
        self.next_move_time = pygame.time.get_ticks()
        self.next_attack_time = pygame.time.get_ticks()
        self.next_get_hit_time = pygame.time.get_ticks()

        self.boss = []
        self.enemies = []
        self.num_enemies = 0
        
        # default stats
        self.lives = 3
        self.atk = 1
        self.armor = 0
        self.atk_range = 30
        self.gold = 0

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def generate_rooms(self):
        # one boss room, 2-3 minigame room, 6-8 loot room, rest regular battle room
        # -1 means completed, 0 means uninitialized, 1 means boss room, 2 means minigame, 3 means loot, 4 means battle
        self.map = [[0 for i in range(5)] for j in range(5)]
        self.adj = [[False for i in range(5)] for j in range(5)]
        self.can_move_next_stage = False
        self.map[2][2] = -1
        while True:
            rand_x = random.randint(0, 4)
            rand_y = random.randint(0, 4)
            if self.map[rand_x][rand_y] == 0:
                self.map[rand_x][rand_y] = 1
                break
        
        num = random.randint(2, 4)
        for i in range(num):
            while True:
                rand_x = random.randint(0, 4)
                rand_y = random.randint(0, 4)
                if self.map[rand_x][rand_y] == 0:
                    self.map[rand_x][rand_y] = 2
                    break
        
        num = random.randint(max(2,3-self.stage//2), max(3,5-self.stage//2))
        for i in range(num):
            while True:
                rand_x = random.randint(0, 4)
                rand_y = random.randint(0, 4)
                if self.map[rand_x][rand_y] == 0:
                    self.map[rand_x][rand_y] = 3
                    break

        for i in range(5):
            for j in range(5):
                if self.map[i][j] == 0:
                    self.map[i][j] = 4

        self.adj[self.roomx-1][self.roomy] = True
        self.adj[self.roomx+1][self.roomy] = True
        self.adj[self.roomx][self.roomy-1] = True
        self.adj[self.roomx][self.roomy+1] = True

    def next_stage(self):
        self.x = self.y = 375
        self.roomx = self.roomy = 2
        self.generate_rooms()

    def can_move_next_room(self):
        if self.num_enemies > 0 or len(self.boss) != 0:
            return -1

        if 310 <= self.x <= 440 and 75 <= self.y <= 90 and self.roomy != 0:
            return 0
        elif 310 <= self.x <= 440 and 610 <= self.y <= 625 and self.roomy != 4:
            return 1
        elif 75 <= self.x <= 90 and 310 <= self.y <= 440 and self.roomx != 0:
            return 2
        elif 635 <= self.x <= 650 and 310 <= self.y <= 440 and self.roomx != 4:
            return 3
        else:
            return -1
        
    def next_room(self):
        if self.map[self.roomx][self.roomy] != 1:
            self.map[self.roomx][self.roomy] = -1

        num = self.can_move_next_room()

        if 0 <= num <= 1:
            self.y = 715-self.y
            self.roomy += (num*2 - 1)
        elif 2 <= num <= 3:
            self.x = 740-self.x
            self.roomx += (num*2 - 5)

        if self.roomx != 0:
            self.adj[self.roomx-1][self.roomy] = True
        if self.roomx != 4:
            self.adj[self.roomx+1][self.roomy] = True
        if self.roomy != 0:
            self.adj[self.roomx][self.roomy-1] = True
        if self.roomy != 4:
            self.adj[self.roomx][self.roomy+1] = True

        # generate enemies
        if self.map[self.roomx][self.roomy] == 4:
            self.can_move = False
            self.num_enemies = random.randint(1,min(10,3+self.stage//2))
            for i in range(self.num_enemies):
                self.enemies.append(Enemy(self.stage))

            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        # generate loot
        if self.map[self.roomx][self.roomy] == 3:
            self.can_move = False
            self.loot = Loot(self.stage)

        # generate boss
        if self.map[self.roomx][self.roomy] == 1 and not self.can_move_next_stage:
            self.can_move = False
            self.boss.append(Boss(self.stage))

            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

    def draw_enemies(self, screen):
        for i in range(self.num_enemies):
            self.enemies[i].move(self.x, self.y)
            self.enemies[i].draw_bg(screen)

            cur_time = pygame.time.get_ticks()
            if cur_time >= self.next_get_hit_time and self.enemies[i].attack(self.x, self.y):
                if self.armor > 0:
                    self.armor -= 1
                else:
                    self.lives -= 1
                self.next_get_hit_time = cur_time + 1500

    def draw_boss(self, screen):
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.boss[0].next_spawn_time:
            self.boss[0].next_spawn_time = cur_time + max(5000,15000-800*self.stage)
            l = self.boss[0].summon()
            for i in range(min(len(l), 10-self.num_enemies)):
                self.enemies.append(l[i])
            self.num_enemies = len(self.enemies)

        self.boss[0].draw_bg(screen)

        if cur_time >= self.next_get_hit_time and self.boss[0].attack(self.x, self.y):
            if self.armor > 0:
                self.armor -= 1
            else:
                self.lives -= 1
            self.next_get_hit_time = cur_time + 1500
        
    def draw_minimap(self, screen):
        for i in range(5):
            for j in range(5):
                if i == self.roomx and j == self.roomy:
                    pygame.draw.rect(screen, CURRENT, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j] == -1:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j] == 1 and self.can_move_next_stage:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                else:
                    pygame.draw.rect(screen, UNKNOWN, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    if self.adj[i][j]:
                        if self.map[i][j] == 1:
                            pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j] == 2:
                            pygame.draw.circle(screen, UNKNOWN_GAME, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j] == 3:
                            pygame.draw.circle(screen, UNKNOWN_LOOT, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j] == 4:
                            pygame.draw.circle(screen, UNKNOWN_BATTLE, (800+31*i+15, 50+31*j+15), 5)

    def draw_stats(self, screen):
        screen.blit(self.my_font.render("lives: " + str(self.lives), True, (0,0,0)), (790,250))
        screen.blit(self.my_font.render("atk:   " + str(self.atk), True, (0,0,0)), (790,300))
        screen.blit(self.my_font.render("armor: " + str(self.armor), True, (0,0,0)), (790,350))
        screen.blit(self.my_font.render("gold:  " + str(self.gold), True, (0,0,0)), (790,400))

    def move(self):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_move_time:
            self.next_move_time = cur_time + 10
            if self.moveU:
                self.y -= 3
            if self.moveD:
                self.y += 3
            if self.moveL:
                self.x -= 3
            if self.moveR:
                self.x += 3
            
        self.y = max(75, self.y)
        self.y = min(625, self.y)
        self.x = max(75, self.x)
        self.x = min(650, self.x)

    def attack(self):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_attack_time:
            self.next_attack_time = cur_time + 1000
            for i in range(self.num_enemies):
                if abs(self.x - self.enemies[i].x) + abs(self.y - self.enemies[i].y) <= self.atk_range:
                    self.enemies[i].hp -= self.atk
                    if self.enemies[i].hp <= 0:
                        self.num_enemies -= 1
                        self.gold += self.enemies[i].max_hp
                        self.enemies.pop(i)
                        break

            if len(self.boss) != 0:
                if abs(self.x - self.boss[0].x) + abs(self.y - self.boss[0].y) <= self.atk_range:
                    self.boss[0].hp -= self.atk
                    if self.boss[0].hp <= 0:
                        self.enemies.clear()
                        self.num_enemies = 0
                        self.gold += self.boss[0].max_hp
                        self.boss.pop(0)
                        self.can_move_next_stage = True
    
    def loot_select(self):
        num = self.loot.select(self.x, self.y)
        if num == 0:
            self.gold += 10+self.stage
        elif num == 1:
            self.atk_range += 10
        elif num == 2:
            self.atk += 2+self.stage//3
        elif num == -2:
            self.atk -= 1+self.stage//3
            self.atk = max(self.atk, 1)

    def draw_bg(self, screen):
        # layout: main game screen + sidebar with minimap, health, items, etc.
        # need to add transitions to each stages in the future

        screen.blit(bg_default, (50,50))

        self.move()
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))

        self.draw_minimap(screen)
        self.draw_stats(screen)
        if len(self.boss) > 0:
            self.draw_boss(screen)

        if self.num_enemies > 0:
            self.draw_enemies(screen)

        if self.map[self.roomx][self.roomy] == 3:
            self.loot.draw_bg(screen, self.x, self.y)

        if self.map[self.roomx][self.roomy] == 1 and self.can_move_next_stage:
            screen.blit(portal_default, (300,300))

        if self.can_move_next_room() != -1:
            screen.blit(self.my_font.render("do u wish to move?", True, (0,0,0)), (250,300))

        screen.blit(person_default, (self.x, self.y))
                
# credits screen
class Credits:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("credits!", True, (0,0,0)), (300,150))
        # insert credits over here and exit button

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("exit?", True, (0,0,0)), (435, 570))
