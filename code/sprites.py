import pygame
import random
from settings import *

# enemies in the game!
class Enemy:
    def __init__(self, stage, money):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawning = True
        self.spawn_time = pygame.time.get_ticks()
        self.next_move_time = self.spawn_time + 2000
        self.hp = self.max_hp = random.randint(2,2+stage)
        self.stage = stage
        self.money = money

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
            l.append(Enemy(self.stage, False))
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
        screen.blit(bg_default, (50,50))
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

# shop after boss
class Shop:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.stage = stage
        self.chosen = [False, False, False]
        self.price = [5*stage, 5*stage, 5*stage]

        for i in range(3):
            self.price[i] += random.randint(15+5*i,25+5*i)

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 32)

    def select(self, person_x, person_y):
        if 180 <= person_x <= 270 and 330 <= person_y <= 420 and not self.chosen[0]:
            self.chosen[0] = True
            return 0
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420 and not self.chosen[1]:
            self.chosen[1] = True
            return 1
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420 and not self.chosen[2]:
            self.chosen[2] = True
            return 2
        elif 280 <= person_x <= 470 and 80 <= person_y <= 270:
            return 3
        else:
            return -1

    def draw_bg(self, screen, person_x, person_y):
        screen.blit(bg_default, (50,50))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 350, 50, 50))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(350, 350, 50, 50))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(500, 350, 50, 50))

        for i in range(3):
            if self.chosen[i]:
                pygame.draw.rect(screen, (100,255,100), pygame.Rect(200+150*i, 350, 50, 50))
            else:
                pygame.draw.rect(screen, (255,100,100), pygame.Rect(200+150*i, 350, 50, 50))

        if 180 <= person_x <= 270 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of longevity", True, (0,0,0)), (100, 550))
            screen.blit(self.my_font.render("cost: " + str(self.price[0]), True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render("restore 2 missing health", True, (0,0,0)), (100, 600))
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of defense", True, (0,0,0)), (100, 550))
            screen.blit(self.my_font.render("cost: " + str(self.price[1]), True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render("gain 1 armor ", True, (0,0,0)), (100, 600))
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            screen.blit(self.my_font.render("blessing of strength", True, (0,0,0)), (100, 550))
            screen.blit(self.my_font.render("cost: " + str(self.price[2]), True, (0,0,0)), (100, 575))
            screen.blit(self.my_font.render("gain 1 attack", True, (0,0,0)), (100, 600))

        screen.blit(portal_default, (300,100))

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
        screen.blit(self.my_font.render("story mode?", True, (0,0,0)), (340, 270))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 400, 600, 100))
        screen.blit(self.my_font.render("endless mode!", True, (0,0,0)), (320, 420))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))

        screen.blit(arrow_default, (80,260+self.option*150))

# types of rooms
class Room:
    def __init__(self, type, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.type = type
        self.stage = stage
        self.cleared = True
        if type == 1 or type == 4:
            self.cleared = False

        self.boss = []
        self.enemies = []
        self.num_enemies = 0

    def attacked(self, damage, atk_range, person_x, person_y):
        for i in range(self.num_enemies):
            if abs(person_x - self.enemies[i].x) + abs(person_y - self.enemies[i].y) <= atk_range:
                self.enemies[i].hp -= damage
                if self.enemies[i].hp <= 0:
                    self.num_enemies -= 1
                    gold = self.enemies[i].max_hp
                    if not self.enemies[i].money:
                        gold = 0
                    self.enemies.pop(i)
                    if len(self.boss) == 0 and self.num_enemies == 0:
                        self.cleared = True
                    return gold

            if len(self.boss) != 0:
                if abs(person_x - self.boss[0].x) + abs(person_y - self.boss[0].y) <= atk_range:
                    self.boss[0].hp -= damage
                    if self.boss[0].hp <= 0:
                        self.enemies.clear()
                        self.num_enemies = 0
                        gold = self.boss[0].max_hp
                        self.boss.pop(0)
                        self.cleared = True
                        return gold
        return -1

    def generate_boss(self):
        self.boss.append(Boss(self.stage))

    def generate_enemies(self):
        self.num_enemies = random.randint(1,min(10,3+self.stage//2))
        for i in range(self.num_enemies):
            self.enemies.append(Enemy(self.stage, True))

    def draw_enemies(self, screen, person_x, person_y):
        attacked = False
        for i in range(self.num_enemies):
            self.enemies[i].move(person_x, person_y)
            self.enemies[i].draw_bg(screen)

            if self.enemies[i].attack(person_x, person_y) and pygame.time.get_ticks() >= self.enemies[i].spawn_time + 2000:
                attacked = True

        return attacked

    def draw_boss(self, screen, person_x, person_y):
        attacked = False
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.boss[0].next_spawn_time:
            self.boss[0].next_spawn_time = cur_time + max(5000,15000-800*self.stage)
            l = self.boss[0].summon()
            for i in range(min(len(l), 10-self.num_enemies)):
                self.enemies.append(l[i])
            self.num_enemies = len(self.enemies)

        self.boss[0].draw_bg(screen)

        if self.boss[0].attack(person_x, person_y):
            attacked = True

        return attacked

    def draw_bg(self, screen, person_x, person_y):
        screen.blit(bg_default, (50,50))
        if self.type == 1 and not self.cleared:
            if self.draw_boss(screen, person_x, person_y):
                return True
        if self.type == 1 or self.type == 4 and not self.cleared:
            if self.draw_enemies(screen, person_x, person_y):
                return True
        if self.type == 1 and self.cleared:
            screen.blit(portal_default, (300,300))

# actual game screen
class Level:
    def __init__(self, gamemode, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.gamemode = gamemode
        self.stage = stage                                       # how deep in the dungeon
        self.rooms_explored = 0
        self.gold_earned = 0
        self.map = [[0 for i in range(5)] for j in range(5)]     # minimap square colours
        self.adj = [[False for i in range(5)] for j in range(5)] # if this room had been adjacent previously

        self.shopping = False
        self.roomx = 2
        self.roomy = 2

        self.x = 375
        self.y = 375

        self.moveU = False
        self.moveD = False
        self.moveL = False
        self.moveR = False

        self.next_move_time = pygame.time.get_ticks()
        self.next_attack_time = pygame.time.get_ticks()
        self.next_get_hit_time = pygame.time.get_ticks()

        # default stats
        self.lives = 3
        self.atk = 1
        self.armor = 0
        self.atk_range = 30
        self.gold = 0

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def generate_rooms(self):
        # one boss room, 2-4 minigame room, 3-5 loot room, rest regular battle room
        # -1 means empty, 0 means uninitialized, 1 means boss room, 2 means minigame, 3 means loot, 4 means battle
        self.x = self.y = 375
        self.roomx = self.roomy = 2
        self.rooms_explored += 1
        self.map = [[0 for i in range(5)] for j in range(5)]
        self.adj = [[False for i in range(5)] for j in range(5)]
        self.can_move_next_stage = False
        self.map[2][2] = Room(-1, self.stage)
        while True:
            rand_x = random.randint(0, 4)
            rand_y = random.randint(0, 4)
            if self.map[rand_x][rand_y] == 0:
                self.map[rand_x][rand_y] = Room(1, self.stage)
                break

        num = random.randint(2, 4)
        for i in range(num):
            while True:
                rand_x = random.randint(0, 4)
                rand_y = random.randint(0, 4)
                if self.map[rand_x][rand_y] == 0:
                    self.map[rand_x][rand_y] = Room(2, self.stage)
                    break

        num = random.randint(max(2,3-self.stage//2), max(3,5-self.stage//2))
        for i in range(num):
            while True:
                rand_x = random.randint(0, 4)
                rand_y = random.randint(0, 4)
                if self.map[rand_x][rand_y] == 0:
                    self.map[rand_x][rand_y] = Room(3, self.stage)
                    break

        for i in range(5):
            for j in range(5):
                if self.map[i][j] == 0:
                    self.map[i][j] = Room(4, self.stage)

        self.adj[self.roomx-1][self.roomy] = True
        self.adj[self.roomx+1][self.roomy] = True
        self.adj[self.roomx][self.roomy-1] = True
        self.adj[self.roomx][self.roomy+1] = True

    def next_stage(self):
        self.x = 375
        self.y = 575
        self.shopping = True
        self.shop = Shop(self.stage)

    def shop_select(self):
        num = self.shop.select(self.x, self.y)
        if num == 0:
            if self.gold >= self.shop.price[0]:
                self.lives = min(3, self.lives+2)
                self.gold -= self.shop.price[0]
            else:
                self.shop.chosen[0] = False
        elif num == 1:
            if self.gold >= self.shop.price[1]:
                self.armor += 1
                self.gold -= self.shop.price[1]
            else:
                self.shop.chosen[1] = False
        elif num == 2:
            if self.gold >= self.shop.price[2]:
                self.atk += 1
                self.gold -= self.shop.price[2]
            else:
                self.shop.chosen[2] = False
        elif num == 3:
            self.shopping = False
            self.stage += 1
            self.generate_rooms()

    def can_move_next_room(self):
        if not self.map[self.roomx][self.roomy].cleared:
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
        if self.map[self.roomx][self.roomy].type != 1:
            self.map[self.roomx][self.roomy] = Room(-1, self.stage)

        num = self.can_move_next_room()

        if 0 <= num <= 1:
            self.y = 715-self.y
            self.roomy += (num*2 - 1)
            self.rooms_explored += 1
        elif 2 <= num <= 3:
            self.x = 740-self.x
            self.roomx += (num*2 - 5)
            self.rooms_explored += 1

        if self.roomx != 0:
            self.adj[self.roomx-1][self.roomy] = True
        if self.roomx != 4:
            self.adj[self.roomx+1][self.roomy] = True
        if self.roomy != 0:
            self.adj[self.roomx][self.roomy-1] = True
        if self.roomy != 4:
            self.adj[self.roomx][self.roomy+1] = True

        # generate enemies
        if self.map[self.roomx][self.roomy].type == 4:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_enemies()
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        # generate loot
        if self.map[self.roomx][self.roomy].type == 3:
            self.can_move = False
            self.loot = Loot(self.stage)

        # generate boss
        if self.map[self.roomx][self.roomy].type == 1 and not self.can_move_next_stage:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_boss()
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

    def draw_minimap(self, screen):
        for i in range(5):
            for j in range(5):
                if i == self.roomx and j == self.roomy:
                    pygame.draw.rect(screen, CURRENT, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j].type == -1:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j].type == 1 and self.map[i][j].cleared:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                else:
                    pygame.draw.rect(screen, UNKNOWN, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    if self.adj[i][j]:
                        if self.map[i][j].type == 1:
                            pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 2:
                            pygame.draw.circle(screen, UNKNOWN_GAME, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 3:
                            pygame.draw.circle(screen, UNKNOWN_LOOT, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 4:
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
            # insert attack animation
            if self.map[self.roomx][self.roomy].type == 1 or self.map[self.roomx][self.roomy].type == 4:
                num = self.map[self.roomx][self.roomy].attacked(self.atk, self.atk_range, self.x, self.y)
                if num > 0:
                    self.gold += num
                    self.gold_earned += num

    def attacked(self):
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.next_get_hit_time:
            if self.armor > 0:
                self.armor -= 1
            else:
                self.lives -= 1
            self.next_get_hit_time = cur_time + 1500

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

        self.move()
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))

        self.draw_minimap(screen)
        self.draw_stats(screen)
        if self.shopping:
            self.shop.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 3:
            self.loot.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].draw_bg(screen, self.x, self.y):
            self.attacked()

        if self.can_move_next_room() != -1:
            screen.blit(self.my_font.render("do u wish to move?", True, (0,0,0)), (250,300))

        screen.blit(person_default, (self.x, self.y))

# game over screen
class End:
    def __init__(self, stage, rooms, gold):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.stage = stage
        self.rooms = rooms
        self.gold = gold

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("game over :(", True, (0,0,0)), (300,150))
        screen.blit(self.my_font.render("stage ended:    " + str(self.stage), True, (0,0,0)), (250,250))
        screen.blit(self.my_font.render("rooms explored: " + str(self.rooms), True, (0,0,0)), (250,325))
        screen.blit(self.my_font.render("gold earned:    " + str(self.gold), True, (0,0,0)), (250,400))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
        screen.blit(arrow_default, (80,560))


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

        screen.blit(arrow_default, (80,260+self.option*120))

# tutorial screen
class Tutorial:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.slide = 1
        self.generating_message = True

        self.stage = 0
        self.map = [[0 for i in range(5)] for j in range(5)]     # minimap square colours
        self.adj = [[False for i in range(5)] for j in range(5)] # if this room had been adjacent previously

        self.shopping = False
        self.roomx = 2
        self.roomy = 2

        self.x = 375
        self.y = 375

        self.moveU = False
        self.moveD = False
        self.moveL = False
        self.moveR = False

        self.next_move_time = pygame.time.get_ticks()
        self.next_attack_time = pygame.time.get_ticks()

        # default stats
        self.lives = 3
        self.atk = 1
        self.armor = 0
        self.atk_range = 30
        self.gold = 0
        self.generate_rooms()

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

    def draw_message(self, screen, message):
        # draw character talking

        # draw textbox
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
        x = 70
        y = 570
        if self.generating_message:
            for i in range(len(message)):
                screen.blit(self.my_font.render(message[i], True, (0,0,0)), (x, y))
                x += 14
                if i % 43 == 42 and not i == 0 and not skip:
                    x = 70
                    y += 30
                pygame.display.flip()
                if message[i] != ' ':
                    pygame.time.wait(25)
                else:
                    skip = False
                    try:
                        position = message.index(' ', i+1)
                        word_length = position - i - 1
                        if (i%43)+word_length > 42 and not i % 43 == 42:
                            x = 70
                            y += 30
                            skip = True
                    except ValueError:
                        position = -1

        else:
            for i in range(len(message)):
                screen.blit(self.my_font.render(message[i], True, (0,0,0)), (x, y))
                x += 14
                if i % 43 == 42 and not i == 0 and not skip:
                    x = 70
                    y += 30
                if message[i] == ' ':
                    skip = False
                    try:
                        position = message.index(' ', i+1)
                        word_length = position - i - 1
                        if (i%43)+word_length > 42 and not i % 43 == 42:
                            x = 70
                            y += 30
                            skip = True
                    except ValueError:
                        position = -1
            screen.blit(self.tiny_font.render("[Press %s To Continue...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))

        self.generating_message = False

    def generate_rooms(self):
        # one boss room, 2-4 minigame room, 3-5 loot room, rest regular battle room
        # -1 means empty, 0 means uninitialized, 1 means boss room, 2 means minigame, 3 means loot, 4 means battle
        self.x = self.y = 375
        self.roomx = self.roomy = 2
        self.map = [[Room(-1, self.stage) for i in range(5)] for j in range(5)]
        self.adj = [[False for i in range(5)] for j in range(5)]
        self.can_move_next_stage = False
        self.map[2][2] = Room(-1, self.stage)
        self.map[2][1] = Room(1, self.stage)
        self.map[1][2] = Room(2, self.stage)
        self.map[3][2] = Room(3, self.stage)
        self.map[2][3] = Room(4, self.stage)

        self.adj[self.roomx-1][self.roomy] = True
        self.adj[self.roomx+1][self.roomy] = True
        self.adj[self.roomx][self.roomy-1] = True
        self.adj[self.roomx][self.roomy+1] = True

    def next_stage(self):
        self.x = 375
        self.y = 575
        self.shopping = True
        self.shop = Shop(self.stage)

    def shop_select(self):
        num = self.shop.select(self.x, self.y)
        if num == 0:
            if self.gold >= self.shop.price[0]:
                self.lives = min(3, self.lives+2)
                self.gold -= self.shop.price[0]
            else:
                self.shop.chosen[0] = False
        elif num == 1:
            if self.gold >= self.shop.price[1]:
                self.armor += 1
                self.gold -= self.shop.price[1]
            else:
                self.shop.chosen[1] = False
        elif num == 2:
            if self.gold >= self.shop.price[2]:
                self.atk += 1
                self.gold -= self.shop.price[2]
            else:
                self.shop.chosen[2] = False
        elif num == 3:
            self.shopping = False
            self.stage += 1
            self.generate_rooms()

    def can_move_next_room(self):
        if not self.map[self.roomx][self.roomy].cleared:
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
        # generate enemies
        if self.map[self.roomx][self.roomy].type == 4:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_enemies()
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        # generate loot
        if self.map[self.roomx][self.roomy].type == 3:
            self.can_move = False
            self.loot = Loot(self.stage)

        # generate boss
        if self.map[self.roomx][self.roomy].type == 1 and not self.can_move_next_stage:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_boss()
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

    def draw_minimap(self, screen):
        for i in range(5):
            for j in range(5):
                if i == self.roomx and j == self.roomy:
                    pygame.draw.rect(screen, CURRENT, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j].type == -1:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j].type == 1 and self.map[i][j].cleared:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                else:
                    pygame.draw.rect(screen, UNKNOWN, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                    if self.adj[i][j]:
                        if self.map[i][j].type == 1:
                            pygame.draw.circle(screen, UNKNOWN_BOSS, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 2:
                            pygame.draw.circle(screen, UNKNOWN_GAME, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 3:
                            pygame.draw.circle(screen, UNKNOWN_LOOT, (800+31*i+15, 50+31*j+15), 5)
                        elif self.map[i][j].type == 4:
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
            # insert attack animation
            if self.map[self.roomx][self.roomy].type == 1 or self.map[self.roomx][self.roomy].type == 4:
                num = self.map[self.roomx][self.roomy].attacked(self.atk, self.atk_range, self.x, self.y)
                if num > 0:
                    self.gold += num

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

    def draw_game_bg(self, screen):
        self.move()
        self.draw_minimap(screen)
        self.draw_stats(screen)
        if self.shopping:
            self.shop.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 3:
            self.loot.draw_bg(screen, self.x, self.y)
        else:
            self.map[self.roomx][self.roomy].draw_bg(screen, self.x, self.y)

        if self.can_move_next_room() != -1:
            screen.blit(self.my_font.render("do u wish to move?", True, (0,0,0)), (250,300))

        screen.blit(person_default, (self.x, self.y))

    def draw_bg(self, screen):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))
        if self.slide == 1:
            self.draw_message(screen, "welcome to minidungeon!")
        elif self.slide == 2:
            self.draw_message(screen, "minidungeon is an endless dungeon crawler game where you will need to fight enemies and earn some loot along the way!")
        elif self.slide == 3:
            self.draw_message(screen, "Use WASD or arrow keys to move. Try it yourself!")
        elif self.slide == 4:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Continue when you are ready!")
        elif self.slide == 5:
            self.draw_game_bg(screen)
            self.draw_message(screen, "You may enter through a door by going near it and pressing %s when given the prompt." % pygame.key.name(CONTROL_CONFIRM[0]))
        elif self.slide == 6:
            self.draw_game_bg(screen)
            self.draw_message(screen, "You cannot travel past the 5x5 grid, nor can you open a door when there are enemies currently in the room with you.")
        elif self.slide == 7:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Notice that you have a 5x5 minimap on your screen! This will serve as a guide for you in the game.")
        elif self.slide == 8:
            self.draw_game_bg(screen)
            self.draw_message(screen, "A red dot = a battle room, a yellow dot = a loot room, a pink dot = a minigame room, and a purple dot = a boss room.")
        elif self.slide == 9:
            self.draw_game_bg(screen)
            self.draw_message(screen, "The number of these rooms are randomized; however, there will only be one boss room.")
        elif self.slide == 10:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Battle rooms contain a random number of enemies that will start chasing you and will attack when they are close enough.")
        elif self.slide == 11:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Press Left-Click on your mouse to attack; note that there is a cooldown to attacks.")
        elif self.slide == 12:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Loot rooms contain three choices of loot by random chance, and you may select one choice using Enter when you are near the black square.")
        elif self.slide == 13:
            self.draw_game_bg(screen)
            self.draw_message(screen, "(insert text about minigame rooms).")
        elif self.slide == 14:
            self.draw_game_bg(screen)
            self.draw_message(screen, "The boss room contains a high-hp boss that will spawn a random number of enemies every once and a while, and you must kill the boss to enter the next stage.")
        elif self.slide == 15:
            self.draw_game_bg(screen)
            self.draw_message(screen, "After each successful boss fight, you will be placed into a shop where you can buy things using gold.")
        elif self.slide == 16:
            self.draw_message(screen, "If you run out of lives, you will be placed into the game over screen, where you can then return to the main menu.")
        elif self.slide == 17:
            self.draw_message(screen, "And that's it! You may now go back to the main menu.")

# credits screen
class Credits:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)
        self.text = pygame.font.SysFont('Calibri', 24)

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("credits!", True, (0,0,0)), (400,150))
        screen.blit(self.text.render("a work-in-progress game made by Eric Ning", True, (0,0,0)), (275,250))
        screen.blit(self.text.render("expected completion date to be by the end of August 2025", True, (0,0,0)), (200,275))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
        screen.blit(arrow_default, (80,560))
