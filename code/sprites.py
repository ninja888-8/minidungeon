import pygame
import math
import random
from settings import *

class Ranged:
    def __init__(self, stage, give_money, current_event):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawning = True
        self.spawn_time = pygame.time.get_ticks()
        self.next_move_time = self.spawn_time + 2000
        self.last_shoot_time = self.spawn_time
        self.hp = self.max_hp = random.randint(1,2+stage)
        self.stage = stage

        if give_money:
            self.money = self.hp
        else:
            self.money = 0
        
        if current_event == 1: # increase health event
            self.hp *= 2
            self.max_hp *= 2
        elif current_event == 2: # increase gold event
            if self.money % 2 == 0:
                self.money *= 1.5
            else:
                self.money *= 1.5
                self.money += 0.5

        self.x = random.randint(100,650)
        self.y = random.randint(100,650)

    def move(self, person_x, person_y):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_move_time:
            self.next_move_time = cur_time + min(15, 30-self.stage/2)
            if person_x != self.x or person_y != self.y:
                choice = random.randint(0,1)
                if choice == 0 or person_y == self.y:
                    if self.x > person_x:
                        self.x += 1
                    elif self.x < person_x:
                        self.x -= 1
                    elif self.x == person_x:
                        choice = 1
                
                if choice == 1:
                    if self.y > person_y:
                        self.y += 1
                    elif self.y < person_y:
                        self.y -= 1

        self.y = max(90, self.y)
        self.y = min(660, self.y)
        self.x = max(90, self.x)
        self.x = min(660, self.x)

    def draw_bg(self, screen):
        screen.blit(archer_slime, (self.x-archer_slime.get_size()[0]/2, self.y-archer_slime.get_size()[1]/2))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-archer_slime.get_size()[0]/2-5, self.y-archer_slime.get_size()[0]/2-10, archer_slime.get_size()[0]+10, 9))
        pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-archer_slime.get_size()[0]/2-3, self.y-archer_slime.get_size()[0]/2-8, (archer_slime.get_size()[0]+6.0)*self.hp/self.max_hp, 5))

# projectiles from ranged enemies
class Projectile:
    def __init__(self, slope, left, x, y):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))

        self.next_move_time = pygame.time.get_ticks()
        self.slope = slope
        self.left = left
        self.x = x
        self.y = y
        
        self.pos = []
        if slope == -100000:
            for i in range(675-y):
                self.pos.append([x,y+2*i])
        elif slope == 100000:
            for i in range(y):
                self.pos.append([x,y-2*i])
        elif not left:
            for i in range(675):
                self.pos.append([x+2*i*math.sqrt(1/(1+slope*slope)), y+slope*2*i*math.sqrt(1/(1+slope*slope))])
        elif left:
            for i in range(675):
                self.pos.append([x-2*i*math.sqrt(1/(1+slope*slope)), y-slope*2*i*math.sqrt(1/(1+slope*slope))])
        self.idx = 0

    def move(self):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_move_time:
            self.next_move_time = cur_time + 1
            self.idx += 1
            if self.idx >= len(self.pos):
                return False
            
        return True

    def attack(self, person_x, person_y):
        if abs(person_x - self.pos[self.idx][0] + 9) + abs(person_y - self.pos[self.idx][1] + 9) <= projectile.get_size()[0]/2 + 8:
            return True
        else:
            return False

    def draw_bg(self, screen):
        screen.blit(projectile, (self.pos[self.idx][0]-projectile.get_size()[0]/2, self.pos[self.idx][1]-projectile.get_size()[1]/2))

# melee enemies in the game!
class Enemy:
    def __init__(self, type, stage, give_money, current_event):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawning = True
        self.spawn_time = pygame.time.get_ticks()
        self.next_move_time = self.spawn_time + 2000

        if type == 0: # regular guy
            self.hp = self.max_hp = random.randint(2,3+stage)
        elif type == 1:
            self.hp = self.max_hp = random.randint(4,6+2*stage)

        self.type = type
        self.stage = stage
        if give_money:
            self.money = self.hp
        else:
            self.money = 0
        
        if current_event == 1: # increase health event
            self.hp *= 2
            self.max_hp *= 2
        elif current_event == 2: # increase gold event
            if self.money % 2 == 0:
                self.money *= 1.5
            else:
                self.money *= 1.5
                self.money += 0.5

        self.x = random.randint(100,650)
        self.y = random.randint(100,650)

    def move(self, person_x, person_y):
        cur_time = pygame.time.get_ticks()

        if cur_time >= self.next_move_time:
            if self.type == 0:
                self.next_move_time = cur_time + min(5, 10-self.stage/2)
            elif self.type == 1:
                self.next_move_time = cur_time + min(10, 20-self.stage/2)

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
        if abs(person_x - self.x) + abs(person_y - self.y) <= (enemy_slime.get_size()[0]/2 + 10 + self.stage):
            return True
        else:
            return False

    def draw_bg(self, screen):
        if self.type == -1:
            screen.blit(enemy_default, (self.x-enemy_default.get_size()[0]/2, self.y-enemy_default.get_size()[1]/2))
        elif self.type == 0:
            screen.blit(enemy_slime, (self.x-enemy_slime.get_size()[0]/2, self.y-enemy_slime.get_size()[1]/2))
        elif self.type == 1:
            screen.blit(enemy_slime_tank, (self.x-enemy_slime_tank.get_size()[0]/2, self.y-enemy_slime_tank.get_size()[1]/2))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-enemy_slime.get_size()[0]/2-5, self.y-enemy_slime.get_size()[0]/2-10, enemy_slime.get_size()[0]+10, 9))
        pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-enemy_slime.get_size()[0]/2-3, self.y-enemy_slime.get_size()[0]/2-8, (enemy_slime.get_size()[0]+6.0)*self.hp/self.max_hp, 5))

# boss enemy in the game
class Boss:
    def __init__(self, type, stage, current_event):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.spawn_time = pygame.time.get_ticks()
        self.next_spawn_time = self.spawn_time + 2000
        self.hp = self.max_hp = 20+8*stage
        self.stage = stage
        self.type = type
        self.money = self.hp // 1.5
        self.current_event = current_event

        if current_event == 1: # increase health event
            self.hp *= 2
            self.max_hp *= 2
        elif current_event == 2: # increase gold event
            if self.money % 2 == 0:
                self.money *= 1.5
            else:
                self.money *= 1.5
                self.money += 0.5

        self.x = 375
        self.y = 375

    def attack(self, person_x, person_y):
        if abs(person_x - self.x) + abs(person_y - self.y) <= boss_slime.get_size()[0]/2 - 5:
            return True
        else:
            return False

    def summon(self):
        l = []
        num = random.randint(2,min(5,3+self.stage//2))
        normal = random.randint(num-2, num)
        for i in range(normal):
            rand = random.randint(1,100)
            if rand > 15:
                l.append(Enemy(0, self.stage, False, self.current_event))
            else:
                l.append(Enemy(1, self.stage, False, self.current_event))
        for i in range((num-normal)//2):
            l.append(Ranged(self.stage, False, self.current_event))
        return l

    def draw_bg(self, screen):
        if self.type == -1:
            screen.blit(enemy_default, (self.x-enemy_default.get_size()[0]/2, self.y-enemy_default.get_size()[1]/2))
        elif self.type == 0:
            screen.blit(boss_slime, (self.x-boss_slime.get_size()[0]/2, self.y-boss_slime.get_size()[1]/2))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-boss_slime.get_size()[0]/2-5, self.y-boss_slime.get_size()[0]/2-10, boss_slime.get_size()[0]+10, 9))
        pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-boss_slime.get_size()[0]/2-3, self.y-boss_slime.get_size()[0]/2-8, (boss_slime.get_size()[0]+6.0)*self.hp/self.max_hp, 5))

# minigame rooms
class Minigame:
    def __init__(self, stage, rooms, gold, enemies):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        if stage != 0:
            self.type = random.randint(0,2)
        else:
            self.type = random.randint(0,1)
        self.selected = False
        self.delay = 0

        self.level = 1
        self.current = -1
        self.gave_money = False

        self.option = 0
        self.choices = [[0 for i in range(3)] for j in range(4)]
        self.rooms = rooms
        self.gold = gold
        self.enemies = enemies
        self.answer = [random.randint(0,3), random.randint(0,3), random.randint(0,3)]

        if self.type == 0:
            self.range_low = random.randint(0,19)
            self.range_high = self.range_low + 10
            self.current = 0
        elif self.type == 1:
            self.x = random.randint(50,700)
            self.y = random.randint(50,600)
            self.time = pygame.time.get_ticks()
        elif self.type == 2:
            for i in range(4):
                if i == self.answer[0]:
                    self.choices[i][0] = self.rooms
                else:
                    self.choices[i][0] = random.randint(-1*self.rooms,15) + self.rooms
                    while self.choices[i][0] == self.rooms:
                        self.choices[i][0] = random.randint(-1*self.rooms,15) + self.rooms
            
            for i in range(4):
                if i == self.answer[1]:
                    self.choices[i][1] = self.gold
                else:
                    self.choices[i][1] = random.randint(-1*self.gold,30) + self.gold
                    while self.choices[i][1] == self.gold:
                        self.choices[i][1] = random.randint(-1*self.gold,30) + self.gold

            for i in range(4):
                if i == self.answer[2]:
                    self.choices[i][2] = self.enemies
                else:
                    self.choices[i][2] = random.randint(-1*self.enemies,15) + self.enemies
                    while self.choices[i][2] == self.enemies:
                        self.choices[i][2] = random.randint(-1*self.enemies,15) + self.enemies

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)
    
    def message(self, screen, won):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
        if won:
            screen.blit(self.my_font.render("you won!", True, (0,0,0)), (100, 575))
        else:
            screen.blit(self.my_font.render("you lost :(", True, (0,0,0)), (100, 575))
        pygame.display.flip()
        pygame.time.wait(1000)

    def select(self, person_x, person_y):
        if 330 <= person_x <= 420 and 330 <= person_y <= 420:
            self.selected = True
            self.delay = pygame.time.get_ticks() + 1000
            self.time = pygame.time.get_ticks() + 1000

    def play(self, screen, mouse_x, mouse_y):
        if self.type == 0:
            if self.range_low <= self.current <= self.range_high or self.range_low <= (59-self.current) <= self.range_high:
                if self.level == 3:
                    self.type = -1
                    if self.current <= 29:
                        pygame.draw.rect(screen, (100,255,100), pygame.Rect(150+15*self.current, 350, 14, 50))
                    else:
                        pygame.draw.rect(screen, (100,255,100), pygame.Rect(150+15*(59-self.current), 350, 14, 50))
                    pygame.display.flip()
                    pygame.time.wait(100)
                else:
                    self.level += 1
                    self.range_low = random.randint(0,19)
                    self.range_high = self.range_low + (9-2*self.level)

            else:
                self.type = -2
                if self.current <= 29:
                    pygame.draw.rect(screen, (255,100,100), pygame.Rect(150+15*self.current, 350, 14, 50))
                else:
                    pygame.draw.rect(screen, (255,100,100), pygame.Rect(150+15*(59-self.current), 350, 14, 50))
                pygame.display.flip()
                pygame.time.wait(100)
        elif self.type == 1:
            if not mouse_x == -1 and not mouse_y == -1:
                if self.x-25 <= mouse_x <= self.x+25 and self.y-25 <= mouse_y <= self.y+25:
                    if self.level == 20:
                        if pygame.time.get_ticks() <= self.time + 12000:
                            self.type = -1
                        else:
                            self.type = -2
                    else:
                        self.level += 1
                        self.x = random.randint(50,700)
                        self.y = random.randint(50,600)
        elif self.type == 2:
            if self.answer[self.level-1] == self.option:
                if self.level == 3:
                    self.type = -1
                else:
                    self.level += 1
                    self.option = 0
            else:
                self.type = -2

    def draw_bg(self, screen, person_x, person_y):
        if self.type == -1 and not self.gave_money:
            self.message(screen, True)
        elif self.type == -2 and not self.gave_money:
            self.message(screen, False)
        elif not self.selected or self.delay > pygame.time.get_ticks():
            if not self.selected:
                screen.blit(minigame_image, (350, 350))
            elif self.type != -2:
                pygame.draw.rect(screen, (100,255,100), pygame.Rect(350, 350, 50, 50))
            else:
                pygame.draw.rect(screen, (255,100,100), pygame.Rect(350, 350, 50, 50))

            if 330 <= person_x <= 420 and 330 <= person_y <= 420:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
                screen.blit(self.tiny_font.render("[Press %s To Select...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
                screen.blit(self.my_font.render("play random minigame? [cost: 5 gold]", True, (0,0,0)), (100, 575))
        elif self.type == 0:
            # timing minigame
            for i in range(30):
                # 15 pixels
                if self.range_low <= i <= self.range_high:
                    pygame.draw.rect(screen, (100,100,127), pygame.Rect(150+15*i, 350, 14, 50))
                else:
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(150+15*i, 350, 14, 50))

            if self.current <= 29:
                pygame.draw.rect(screen, (255,255,100), pygame.Rect(150+15*self.current, 350, 14, 50))
            else:
                pygame.draw.rect(screen, (255,255,100), pygame.Rect(150+15*(59-self.current), 350, 14, 50))
            pygame.display.flip()
            pygame.time.wait(10)
            self.current += 1
            self.current %= 60
        elif self.type == 1:
            # aim minigame
            pygame.draw.rect(screen, (255,100,100), pygame.Rect(self.x-25,self.y-25,50,50))
            pygame.draw.rect(screen, (100,100,127), pygame.Rect(self.x-22,self.y-22,44,44))

            pygame.draw.rect(screen, (0,0,0), pygame.Rect(50, 650, 650, 50))
            pygame.draw.rect(screen, (255,100,100), pygame.Rect(55, 655, (640.0)*(12000-pygame.time.get_ticks()+self.time)/12000, 40))

            if pygame.time.get_ticks() > self.time + 12000:
                self.type = -2
                self.message(screen, False)

        elif self.type == 2:
            # trivia minigame (3 questions, num rooms? enemies? num X rooms?)
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Select...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            if self.level == 1:
                screen.blit(self.my_font.render("how many rooms have you explored?", True, (0,0,0)), (75, 575))
                screen.blit(self.my_font.render("(including the shops)", True, (0,0,0)), (75, 600))
            elif self.level == 2:
                screen.blit(self.my_font.render("how much gold have you earned?", True, (0,0,0)), (75, 575))
            elif self.level == 3:
                screen.blit(self.my_font.render("how many regular enemies have you encountered?", True, (0,0,0)), (75, 575))

            for i in range(4):
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 100 + i*100, 650, 75))
                screen.blit(self.my_font.render(str(self.choices[i][self.level-1]), True, (0,0,0)), (400, 110 + i*100))
            screen.blit(arrow_default, (80,100+self.option*100))
            screen.blit(arrow_2_default, (820,100+self.option*100))

# loot rooms
class Loot:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.can_choose = True
        self.chosen = -1
        self.success = True
        self.stage = stage

        self.names = ["wealth", "life", "power", "defence", "luck", "range"]
        self.chances = [50, 40, 30, 30, 5, 15] 
        self.indices = [random.randint(0,1), random.randint(2,3), random.randint(4,5)]

        for i in range(6):
            self.chances[i] = max(self.chances[i], random.randint(self.chances[i], 100) - self.stage)

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

    def select(self, person_x, person_y):
        num = random.randint(0,100)
        if not self.can_choose:
            return -1
        elif 180 <= person_x <= 270 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 0
            if num <= self.chances[self.indices[0]]:
                return 0
            else:
                self.success = False
                return -1
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 1
            if num <= self.chances[self.indices[1]]:
                return 1
            else:
                self.success = False
                return -1
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            self.can_choose = False
            self.chosen = 2
            if num <= self.chances[self.indices[2]]:
                return 2
            else:
                self.success = False
                return -2
        else:
            return -1

    def draw_bg(self, screen, person_x, person_y):
        if self.indices[0] == 0:
            screen.blit(gain_gold, (200,350))
        else:
            screen.blit(gain_life, (200,350))
        if self.indices[1] == 2:
            screen.blit(gain_range, (350,350))
        else:
            screen.blit(gain_def, (350,350))
        if self.indices[2] == 4:
            screen.blit(gain_atk, (500,350))
        else:
            screen.blit(gain_range, (500,350))

        if self.chosen != -1:
            if self.success:
                pygame.draw.rect(screen, (100,255,100), pygame.Rect(200+150*self.chosen, 350, 50, 50))
            else:
                pygame.draw.rect(screen, (255,100,100), pygame.Rect(200+150*self.chosen, 350, 50, 50))

        if 180 <= person_x <= 270 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Select...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of " + str(self.names[self.indices[0]]), True, (0,0,0)), (75, 575))
            if self.indices[0] == 0:
                screen.blit(self.my_font.render(str(self.chances[0]) + "% to gain " + str(10+self.stage) + " gold", True, (0,0,0)), (75, 600))
            else:
                screen.blit(self.my_font.render(str(self.chances[1]) + "% to gain a missing life", True, (0,0,0)), (75, 600))
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Select...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of " + str(self.names[self.indices[1]]), True, (0,0,0)), (75, 575))
            if self.indices[1] == 2:
                screen.blit(self.my_font.render(str(self.chances[2]) + "% to gain 5 atk range", True, (0,0,0)), (75, 600))
            else:
                screen.blit(self.my_font.render(str(self.chances[3]) + "% to gain 1 defence (blocks 1 hit)", True, (0,0,0)), (75, 600))
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Select...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of " + str(self.names[self.indices[2]]), True, (0,0,0)), (75, 575))
            if self.indices[2] == 4:
                screen.blit(self.my_font.render(str(self.chances[4]) + "% to gain " + str(1.5+self.stage//3) + " atk (otherwise lose " + str(1+self.stage//3) + ")", True, (0,0,0)), (75, 600))
            else:
                screen.blit(self.my_font.render(str(self.chances[5]) + "% to gain " + str(10+self.stage//3) + " atk range (otherwise lose " + str(8+self.stage//3) + ")", True, (0,0,0)), (75, 600))
        
# shop after boss
class Shop:
    def __init__(self, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.stage = stage
        self.chosen = [False, False, False]
        self.price = [5*stage, 5*stage, 5*stage]

        for i in range(3):
            self.price[i] += random.randint(15+7*i,25+7*i)

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

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
        screen.blit(gain_life, (200,350))
        screen.blit(gain_def, (350,350))
        screen.blit(gain_atk, (500,350))

        for i in range(3):
            if self.chosen[i]:
                pygame.draw.rect(screen, (100,255,100), pygame.Rect(200+150*i, 350, 50, 50))

        if 180 <= person_x <= 270 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Purchase...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of longevity", True, (0,0,0)), (75, 575))
            screen.blit(self.my_font.render("cost: " + str(self.price[0]), True, (0,0,0)), (75, 600))
            screen.blit(self.my_font.render("restore 2 missing health", True, (0,0,0)), (75, 625))
        elif 330 <= person_x <= 420 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Purchase...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of defence", True, (0,0,0)), (75, 575))
            screen.blit(self.my_font.render("cost: " + str(self.price[1]), True, (0,0,0)), (75, 600))
            screen.blit(self.my_font.render("gain 1 defence ", True, (0,0,0)), (75, 625))
        elif 480 <= person_x <= 570 and 330 <= person_y <= 420:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Purchase...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (450, 670))
            screen.blit(self.my_font.render("blessing of strength", True, (0,0,0)), (75, 575))
            screen.blit(self.my_font.render("cost: " + str(self.price[2]), True, (0,0,0)), (75, 600))
            screen.blit(self.my_font.render("gain 1 attack", True, (0,0,0)), (75, 625))
        elif 280 <= person_x <= 470 and 80 <= person_y <= 270:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.tiny_font.render("[Press %s To Continue To Next Stage...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (350, 670))
            screen.blit(self.my_font.render("[???]", True, (0,0,0)), (75, 575))

        screen.blit(portal_default, (300,100))

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
        self.projectiles = []
        self.num_enemies = 0

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

    def attacked(self, damage, atk_range, person_x, person_y):
        for i in range(self.num_enemies):
            if abs(person_x - self.enemies[i].x) + abs(person_y - self.enemies[i].y) <= atk_range:
                self.enemies[i].hp -= damage
                if self.enemies[i].hp <= 0:
                    self.num_enemies -= 1
                    gold = self.enemies[i].money
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
                    gold = self.boss[0].money
                    self.boss.pop(0)
                    self.cleared = True
                    return gold 
        return -1

    def generate_boss(self, current_event):
        self.boss.append(Boss(0, self.stage, current_event))

    def generate_enemies(self, current_event):
        self.num_enemies = random.randint(1,min(12,4+self.stage//2))
        normal = random.randint(0,self.num_enemies)
        for i in range(normal):
            num = random.randint(1,100)
            if num > 15:
                self.enemies.append(Enemy(0, self.stage, True, current_event))
            else:
                self.enemies.append(Enemy(1, self.stage, True, current_event))
        for i in range(math.ceil((self.num_enemies-normal)/2)):
            self.enemies.append(Ranged(self.stage, True, current_event))
        self.num_enemies = len(self.enemies)

        return self.num_enemies

    def draw_enemies(self, screen, person_x, person_y):
        attacked = False
        for i in range(self.num_enemies):
            self.enemies[i].move(person_x, person_y)
            self.enemies[i].draw_bg(screen)

            if type(self.enemies[i]) is Enemy and self.enemies[i].attack(person_x, person_y) and pygame.time.get_ticks() >= self.enemies[i].spawn_time + 2000:
                attacked = True
            elif type(self.enemies[i]) is Ranged and pygame.time.get_ticks() >= self.enemies[i].spawn_time + max(2000, 3000 - 100*self.stage) and pygame.time.get_ticks() >= self.enemies[i].last_shoot_time + max(2000, 3000 - 100*self.stage):
                if not person_x == self.enemies[i].x:
                    self.projectiles.append(Projectile((person_y-self.enemies[i].y)/(person_x-self.enemies[i].x), self.enemies[i].x >= person_x, self.enemies[i].x, self.enemies[i].y))
                elif person_y >= self.enemies[i].y:
                    self.projectiles.append(Projectile(-100000, self.enemies[i].x >= person_x, self.enemies[i].x, self.enemies[i].y))
                else:
                    self.projectiles.append(Projectile(100000, self.enemies[i].x >= person_x, self.enemies[i].x, self.enemies[i].y))
                self.enemies[i].last_shoot_time = pygame.time.get_ticks() + max(2000, 3000 - 100*self.stage)
        
        for i in range(len(self.projectiles)):
            if i >= len(self.projectiles):
                break
            if not self.projectiles[i].move():
                self.projectiles.pop(i)
                i -= 1
            else:
                self.projectiles[i].draw_bg(screen)
                if self.projectiles[i].attack(person_x, person_y):
                    attacked = True

                if not 75 <= self.projectiles[i].x <= 675:
                    self.projectiles.pop(i)

                i -= 1

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
        if self.type == 1 and not self.cleared:
            if self.draw_boss(screen, person_x, person_y):
                return True
        if self.type == 1 or self.type == 4 and not self.cleared:
            if self.draw_enemies(screen, person_x, person_y):
                return True
        if self.type == 1 and self.cleared:
            screen.blit(portal_default, (300,300))

            if 280 <= person_x <= 470 and 280 <= person_y <= 470:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
                screen.blit(self.tiny_font.render("[Press %s To Continue To Shop...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (375, 670))
                screen.blit(self.my_font.render("[???]", True, (0,0,0)), (75, 575))
        
# actual game screen
class Level:
    def __init__(self, gamemode, stage):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.gamemode = gamemode
        self.stage = stage                                       # how deep in the dungeon
        self.rooms_explored = 0
        self.gold_earned = 0
        self.enemies_encountered = 0
        self.map = [[0 for i in range(5)] for j in range(5)]     # minimap square colours
        self.vis = [[False for i in range(5)] for j in range(5)] # if this room had been visited previously
        self.adj = [[False for i in range(5)] for j in range(5)] # if this room had been adjacent previously

        self.message = False
        self.shopping = False
        self.roomx = 2
        self.roomy = 2
        self.current_event = 0

        self.x = 375
        self.y = 375

        self.moveU = False
        self.moveD = False
        self.moveL = False
        self.moveR = False

        self.next_move_time = pygame.time.get_ticks()
        self.next_attack_time = pygame.time.get_ticks()
        self.next_get_hit_time = pygame.time.get_ticks()
        self.animation_frame = -1
        self.atk_x = -1
        self.atk_y = -1
        
        # default stats
        self.lives = 3
        self.atk = 5
        self.defence = 0
        self.atk_range = 50
        self.gold = 5

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

    def generate_rooms(self):
        # one boss room, 2-4 minigame room, 3-5 loot room, rest regular battle room
        # -1 means empty, 0 means uninitialized, 1 means boss room, 2 means minigame, 3 means loot, 4 means battle
        self.x = self.y = 375
        self.roomx = self.roomy = 2
        self.rooms_explored += 1
        self.map = [[0 for i in range(5)] for j in range(5)]
        self.vis = [[False for i in range(5)] for j in range(5)]
        self.adj = [[False for i in range(5)] for j in range(5)]
        self.can_move_next_stage = False
        self.map[2][2] = Room(-1, self.stage)
        self.vis[2][2] = True

        if self.gamemode == 0 and self.stage == 2:
            self.map[4][2] = Room(1, 5) # ups the difficulty from 2 to 5
        else:
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
                self.defence += 1
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

        if 310 <= self.x <= 440 and 90 <= self.y <= 100:
            if self.roomy != 0:
                return 0
            else:
                return -2
        elif 310 <= self.x <= 440 and 650 <= self.y <= 660:
            if self.roomy != 4:
                return 1
            else:
                return -2
        elif 90 <= self.x <= 100 and 310 <= self.y <= 440:
            if self.roomx != 0:
                return 2
            else:
                return -2
        elif 650 <= self.x <= 660 and 310 <= self.y <= 440:
            if self.roomx != 4:
                return 3
            else:
                if self.gamemode == 0 and self.stage == 2:
                    return 4
                else:
                    return -2
        else:
            return -1
        
    def next_room(self):
        if self.map[self.roomx][self.roomy].type != 1:
            self.vis[self.roomx][self.roomy] = True

        num = self.can_move_next_room()

        if 0 <= num <= 1:
            self.y = 715-self.y
            self.roomy += (num*2 - 1)
            if not self.vis[self.roomx][self.roomy]:
                self.rooms_explored += 1
        elif 2 <= num <= 3:
            self.x = 740-self.x
            self.roomx += (num*2 - 5)
            if not self.vis[self.roomx][self.roomy]:
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
        if self.map[self.roomx][self.roomy].type == 4 and not self.vis[self.roomx][self.roomy]:
            # check if event occured
            temp = random.randint(1,100)
            if temp <= 20:
                self.current_event = random.randint(1,4)
                if self.current_event == 4: # doubles chance for 2x health without affecting others
                    self.current_event == 1

            self.can_move = False
            self.enemies_encountered += self.map[self.roomx][self.roomy].generate_enemies(self.current_event)
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        # generate loot
        if self.map[self.roomx][self.roomy].type == 3 and not self.vis[self.roomx][self.roomy]:
            self.can_move = False
            self.map[self.roomx][self.roomy].loot = Loot(self.stage)

        # generate minigame
        if self.map[self.roomx][self.roomy].type == 2 and not self.vis[self.roomx][self.roomy]:
            self.map[self.roomx][self.roomy].minigame = Minigame(self.stage, self.rooms_explored, self.gold_earned, self.enemies_encountered)

        # generate boss
        if self.map[self.roomx][self.roomy].type == 1 and not self.can_move_next_stage:
            # check if event occured
            temp = random.randint(1,100)
            if temp <= 20:
                if self.current_event == 4: # doubles chance for 2x health without affecting others
                    self.current_event == 1

            self.can_move = False
            self.map[self.roomx][self.roomy].generate_boss(self.current_event)
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000
        
    def draw_minimap(self, screen):
        for i in range(5):
            for j in range(5):
                if i == self.roomx and j == self.roomy:
                    pygame.draw.rect(screen, CURRENT, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.vis[i][j]:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
                elif self.map[i][j].type == 1 and self.map[i][j].cleared:
                    pygame.draw.rect(screen, VISITED, pygame.Rect(800+31*i, 50+31*j, 30, 30))
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
        screen.blit(self.my_font.render("lives: " + str(self.lives), True, (0,0,0)), (800,250))
        screen.blit(self.my_font.render("atk:   " + str(self.atk), True, (0,0,0)), (800,300))
        screen.blit(self.my_font.render("def:   " + str(self.defence), True, (0,0,0)), (800,350))
        screen.blit(self.my_font.render("gold:  " + str(self.gold), True, (0,0,0)), (800,400))

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
            
        self.y = max(90, self.y)
        self.y = min(660, self.y)
        self.x = max(90, self.x)
        self.x = min(660, self.x)

    def attack(self):
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.next_attack_time:
            self.next_attack_time = cur_time + 1000
            self.animation_frame = 25 * person_type1.get_size()[0] // (self.atk_range-15)
            self.atk_x = self.x
            self.atk_y = self.y
            if self.map[self.roomx][self.roomy].type == 1 or self.map[self.roomx][self.roomy].type == 4:
                num = self.map[self.roomx][self.roomy].attacked(self.atk, self.atk_range, self.x, self.y)
                if num > 0:
                    self.gold += num
                    self.gold_earned += num
                    self.gold = round(self.gold)
                    self.gold_earned = round(self.gold_earned)
                
                if self.map[self.roomx][self.roomy].cleared:
                    self.current_event = 0

    def attacked(self):
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.next_get_hit_time:
            if self.defence > 0:
                self.defence -= 1
            else:
                self.lives -= 1
            self.next_get_hit_time = cur_time + 1500
    
    def loot_select(self):
        num = self.map[self.roomx][self.roomy].loot.select(self.x, self.y)
        if num == 0:
            if self.map[self.roomx][self.roomy].loot.indices[0] == 0:
                self.gold += 10+self.stage
                self.gold_earned += 10+self.stage
            else:
                self.lives += 1
                self.lives = min(3, self.lives)
        elif num == 1:
            if self.map[self.roomx][self.roomy].loot.indices[1] == 2:
                self.atk_range += 5
            else:
                self.defence += 1
        elif num == 2:
            if self.map[self.roomx][self.roomy].loot.indices[2] == 4:
                self.atk += 1.5+self.stage//3
            else:
                self.atk_range += 10+self.stage//3
        elif num == -2:
            if self.map[self.roomx][self.roomy].loot.indices[2] == 4:
                self.atk -= 1+self.stage//3
                self.atk = max(self.atk, 1)
            else:
                self.atk_range -= 8+self.stage//3
                self.atk_range = max(self.atk_range, 30)

    def minigame_select(self, mouse_x, mouse_y):
        if not self.map[self.roomx][self.roomy].minigame.selected and self.gold >= 5:
            self.map[self.roomx][self.roomy].minigame.select(self.x, self.y)
            if self.map[self.roomx][self.roomy].minigame.selected:
                self.gold -= 5
        elif self.map[self.roomx][self.roomy].minigame.selected:
            self.map[self.roomx][self.roomy].minigame.play(self.screen, mouse_x, mouse_y)

    def draw_bg(self, screen):
        # layout: main game screen + sidebar with minimap, health, items, etc.
        # need to add transitions to each stages in the future

        if self.gamemode == 0 and self.stage == 2:
            screen.fill(BG_RED)

        self.move()
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))

        self.draw_minimap(screen)
        self.draw_stats(screen)
        if self.shopping:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_default_2_danger, (50,50))
            else:
                screen.blit(bg_default_2, (50,50))
            self.shop.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 3:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_default_2_danger, (50,50))
            else:
                screen.blit(bg_default_2, (50,50))
            self.map[self.roomx][self.roomy].loot.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 2:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_default_danger, (50,50))
            else:
                screen.blit(bg_default, (50,50))
            self.map[self.roomx][self.roomy].minigame.draw_bg(screen, self.x, self.y)
            if not self.map[self.roomx][self.roomy].minigame.gave_money and self.map[self.roomx][self.roomy].minigame.type == -1:
                self.gold += 10
                self.gold_earned += 10
                self.map[self.roomx][self.roomy].minigame.gave_money = True
            elif not self.map[self.roomx][self.roomy].minigame.gave_money and self.map[self.roomx][self.roomy].minigame.type == -2:
                self.map[self.roomx][self.roomy].minigame.gave_money = True
        elif self.map[self.roomx][self.roomy].type == 1:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_boss_danger, (50,50))
            else:
                screen.blit(bg_boss, (50,50))
        elif self.map[self.roomx][self.roomy].type == 4:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_battle_danger, (50,50))
            else:
                screen.blit(bg_battle, (50,50))
        else:
            if self.gamemode == 0 and self.stage == 2:
                screen.blit(bg_default_danger, (50,50))
            else:
                screen.blit(bg_default, (50,50))

        if self.animation_frame != -1 and not self.map[self.roomx][self.roomy].type == 2:
            pygame.draw.circle(screen, (255,127,127), (self.atk_x,self.atk_y), (int)(min(self.animation_frame,50)/50.0 * (self.atk_range-15)))
            self.animation_frame += 1
            if self.animation_frame == 100 + 25 * person_type1.get_size()[0] // (self.atk_range-15):
                self.animation_frame = -1

        if (self.map[self.roomx][self.roomy].type == 1 or self.map[self.roomx][self.roomy].type == 4) and not self.shopping and self.map[self.roomx][self.roomy].draw_bg(screen, self.x, self.y):
            self.attacked()

        num = self.can_move_next_room()
        if 0 <= num <= 3:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(30, 690, 690, 45))
            screen.blit(self.my_font.render("do you wish to move?", True, (0,0,0)), (50,700))
            screen.blit(self.tiny_font.render("[Press %s To Continue...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (470, 705))
        elif num == -2:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(30, 690, 690, 45))
            screen.blit(self.my_font.render("you can't ... escape .....", True, (0,0,0)), (50,700))
            screen.blit(self.tiny_font.render("[P{@s$ / |- #@nt!^*e...]", True, (0,0,0)), (470, 705))
        elif num == 4:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(30, 690, 690, 45))
            screen.blit(self.my_font.render("you can? ... escape .....?", True, (0,0,0)), (50,700))
            screen.blit(self.tiny_font.render("[P{es$ %s to C@nt!^ue...]" % pygame.key.name(CONTROL_CONFIRM[0]), True, (0,0,0)), (470, 705))

        if self.map[self.roomx][self.roomy].type == 2:
            if not self.map[self.roomx][self.roomy].minigame.selected or self.map[self.roomx][self.roomy].minigame.type < 0 or not self.map[self.roomx][self.roomy].type == 2:
                screen.blit(person_type1, (self.x-person_type1.get_size()[0]/2, self.y-person_type1.get_size()[1]/2))
        else:
            screen.blit(person_type1, (self.x-person_type1.get_size()[0]/2, self.y-person_type1.get_size()[1]/2))
        
        if self.current_event == 1: # enemy health increase
            screen.blit(self.my_font.render("EVENT!", True, (0,0,0)), (840,600))
            screen.blit(self.my_font.render("2x enemy hp ...", True, (0,0,0)), (770,650))
        elif self.current_event == 2: # extra gold !!
            screen.blit(self.my_font.render("EVENT!", True, (0,0,0)), (840,600))
            screen.blit(self.my_font.render("earn 1.5x gold!!", True, (0,0,0)), (765,650))
        elif self.current_event == 3: # darkness :)
            screen.blit(self.my_font.render("EVENT!", True, (0,0,0)), (840,600))
            screen.blit(self.my_font.render("darkness uh oh..", True, (0,0,0)), (765,650))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, max(0,self.x-100), WINDOW_HEIGHT))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x+100, 0, max(0,WINDOW_HEIGHT-(self.x+100)), WINDOW_HEIGHT))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, WINDOW_HEIGHT, max(0,self.y-100)))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, self.y+100, WINDOW_HEIGHT, max(0,WINDOW_HEIGHT-(self.y+100))))

        if self.gamemode == 0 and self.stage == 2 and not self.message:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
            screen.blit(self.my_font.render("something doesn't feel right ...", True, (0,0,0)), (100, 575))
            pygame.display.flip()
            pygame.time.wait(2000)
            self.message = True
            pygame.event.clear()
                
# game over screen
class End:
    def __init__(self, stage, rooms, gold, ending):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.stage = stage
        self.rooms = rooms
        self.gold = gold
        self.ending = ending

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

    def draw_cutscene(self, screen):
        if self.ending == 1:
            # draw the character moving up to the house

            # start x = 440, y = 700 --> goes up to y = 340
        elif self.ending == 2:
            # start x = 470, y = 700 --> goes up to y = 250

    def draw_bg(self, screen):
        if self.ending == 0:
            screen.blit(self.my_font.render("game over :(", True, (0,0,0)), (300,150))
        elif self.ending == 1:
            screen.blit(self.my_font.render("you.. escaped?", True, (0,0,0)), (280,150))
        elif self.ending == 2:
            screen.blit(self.my_font.render("you escaped!!", True, (0,0,0)), (290,150))
        screen.blit(self.my_font.render("stage ended:    " + str(self.stage), True, (0,0,0)), (250,250))
        screen.blit(self.my_font.render("rooms explored: " + str(self.rooms), True, (0,0,0)), (250,325))
        screen.blit(self.my_font.render("gold earned:    " + str(self.gold), True, (0,0,0)), (250,400))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
        screen.blit(arrow_default, (80,560))
        screen.blit(arrow_2_default, (820,560))

# game select screen
class Select:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.option = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)

        self.buttons = ["normal mode!", "endless mode!", "return to main menu?"]
        self.locations = [330, 320, 220] # x coordinates of text

    def button_animation(self, screen, option):
        for _ in range(2):
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 250+150*option, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(200+i, 250+i+150*option, 600-2*i, 100-2*i))
                screen.blit(self.my_font.render(self.buttons[option], True, (0,0,0)), (self.locations[option], 270+150*option))
                pygame.display.flip()
                pygame.time.wait(20)
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 250+150*option, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(210-i, 260-i+150*option, 580+2*i, 80+2*i))
                screen.blit(self.my_font.render(self.buttons[option], True, (0,0,0)), (self.locations[option], 270+150*option))
                pygame.display.flip()
                pygame.time.wait(20)
        pygame.event.clear()

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("mini dungeon level select!", True, (0,0,0)), (200,125))
        
        for i in range(3):
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 250+150*i, 600, 100))
            screen.blit(self.my_font.render(self.buttons[i], True, (0,0,0)), (self.locations[i], 270+150*i))

        screen.blit(arrow_default, (80,260+self.option*150))
        screen.blit(arrow_2_default, (820,260+self.option*150))

# Main menu screen
class Menu:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.option = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)
        self.title = pygame.font.SysFont('Calibri', 86)

        self.buttons = ["tutorial?", "play!", "credits?", "exit?"]
        self.locations = [400, 440, 400, 440] # x coordinates of text

    def button_animation(self, screen, option):
        for _ in range(2):
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 250+120*option, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(200+i, 250+i+120*option, 600-2*i, 100-2*i))
                screen.blit(self.my_font.render(self.buttons[option], True, (0,0,0)), (self.locations[option], 270+120*option))
                pygame.display.flip()
                pygame.time.wait(20)
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 250+120*option, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(210-i, 260-i+120*option, 580+2*i, 80+2*i))
                screen.blit(self.my_font.render(self.buttons[option], True, (0,0,0)), (self.locations[option], 270+120*option))
                pygame.display.flip()
                pygame.time.wait(20)
        pygame.event.clear()

    def draw_bg(self, screen):
        screen.blit(self.title.render("mini dungeon!", True, (0,0,0)), (250,100))
        screen.blit(background_slime_1, (50,50))
        screen.blit(background_slime_2, (850,50))
        
        for i in range(4):
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 250+120*i, 600, 100))
            screen.blit(self.my_font.render(self.buttons[i], True, (0,0,0)), (self.locations[i], 270+120*i))

        screen.blit(arrow_default, (80,260+self.option*120))
        screen.blit(arrow_2_default, (820,260+self.option*120))

        # achievements 
        screen.blit(achievement_box, (900,650))

# tutorial screen
class Tutorial:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.slide = 1
        self.generating_message = True

        self.stage = 0
        self.map = [[0 for i in range(5)] for j in range(5)]     # minimap square colours
        self.vis = [[False for i in range(5)] for j in range(5)] # if this room had been visited previously
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
        self.animation_frame = -1
        self.atk_x = -1
        self.atk_y = -1
        
        # default stats
        self.lives = 3
        self.atk = 1
        self.defence = 0
        self.atk_range = 50
        self.gold = 0
        self.generate_rooms()

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Courier New', 24)
        self.tiny_font = pygame.font.SysFont('Courier New', 14)

    def draw_message(self, screen, message):
        # draw textbox
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(50, 550, 650, 150))
        x = 70
        y = 570
        if self.generating_message:
            for i in range(len(message)):
                if (not (message[i] == ' ' and x == 70)):
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
            
            pygame.event.clear()

        else:
            for i in range(len(message)):
                if (not (message[i] == ' ' and x == 70)):
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
        self.vis = [[False for i in range(5)] for j in range(5)]
        self.adj = [[False for i in range(5)] for j in range(5)]
        self.vis[2][2] = True
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

    def can_move_next_room(self):
        if not self.map[self.roomx][self.roomy].cleared:
            return -1

        if 310 <= self.x <= 440 and 90 <= self.y <= 100 and self.roomy != 0:
            return 0
        elif 310 <= self.x <= 440 and 650 <= self.y <= 660 and self.roomy != 4:
            return 1
        elif 90 <= self.x <= 100 and 310 <= self.y <= 440 and self.roomx != 0:
            return 2
        elif 650 <= self.x <= 660 and 310 <= self.y <= 440 and self.roomx != 4:
            return 3
        else:
            return -1
        
    def next_room(self):
        # generate enemies
        if self.map[self.roomx][self.roomy].type == 4 and not self.vis[self.roomx][self.roomy]:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_enemies(0)
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        # generate loot
        if self.map[self.roomx][self.roomy].type == 3 and not self.vis[self.roomx][self.roomy]:
            self.can_move = False
            self.map[self.roomx][self.roomy].loot = Loot(self.stage)

        # generate minigame
        if self.map[self.roomx][self.roomy].type == 2 and not self.vis[self.roomx][self.roomy]:
            self.map[self.roomx][self.roomy].minigame = Minigame(0,0,0,0)

        # generate boss
        if self.map[self.roomx][self.roomy].type == 1 and not self.can_move_next_stage:
            self.can_move = False
            self.map[self.roomx][self.roomy].generate_boss(0)
            cur_time = pygame.time.get_ticks()
            self.next_get_hit_time = cur_time + 2000
            self.next_attack_time = cur_time + 2000

        self.vis[self.roomx][self.roomy] = True
        
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
        screen.blit(self.my_font.render("lives: " + str(self.lives), True, (0,0,0)), (800,250))
        screen.blit(self.my_font.render("atk:   " + str(self.atk), True, (0,0,0)), (800,300))
        screen.blit(self.my_font.render("def:   " + str(self.defence), True, (0,0,0)), (800,350))
        screen.blit(self.my_font.render("gold:  " + str(self.gold), True, (0,0,0)), (800,400))

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
            
        self.y = max(90, self.y)
        self.y = min(660, self.y)
        self.x = max(90, self.x)
        self.x = min(660, self.x)

    def attack(self):
        cur_time = pygame.time.get_ticks()
        if cur_time >= self.next_attack_time:
            self.next_attack_time = cur_time + 1000
            self.animation_frame = 25 * person_type1.get_size()[0] // (self.atk_range-15)
            self.atk_x = self.x
            self.atk_y = self.y
            if self.map[self.roomx][self.roomy].type == 1 or self.map[self.roomx][self.roomy].type == 4:
                num = self.map[self.roomx][self.roomy].attacked(self.atk, self.atk_range, self.x, self.y)
                if num > 0:
                    self.gold += num
    
    def draw_game_bg(self, screen):
        # layout: main game screen + sidebar with minimap, health, items, etc.
        # need to add transitions to each stages in the future

        self.move()
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))

        self.draw_minimap(screen)
        self.draw_stats(screen)
        if self.shopping:
            screen.blit(bg_default_2, (50,50))
            self.shop.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 3:
            screen.blit(bg_default_2, (50,50))
            self.map[self.roomx][self.roomy].loot.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 2:
            screen.blit(bg_default, (50,50))
            self.map[self.roomx][self.roomy].minigame.draw_bg(screen, self.x, self.y)
        elif self.map[self.roomx][self.roomy].type == 1:
            screen.blit(bg_boss, (50,50))
        elif self.map[self.roomx][self.roomy].type == 4:
            screen.blit(bg_battle, (50,50))
        else:
            screen.blit(bg_default, (50,50))
        self.map[self.roomx][self.roomy].draw_bg(screen, self.x, self.y)

        if self.animation_frame != -1 and not self.map[self.roomx][self.roomy].type == 2:
            pygame.draw.circle(screen, (255,127,127), (self.atk_x,self.atk_y), (int)(min(self.animation_frame,50)/50.0 * (self.atk_range-15)))
            self.animation_frame += 1
            if self.animation_frame == 100 + 25 * person_type1.get_size()[0] // (self.atk_range-15):
                self.animation_frame = -1

        if self.can_move_next_room() != -1:
            screen.blit(self.my_font.render("do u wish to move?", True, (0,0,0)), (250,350))

        screen.blit(person_type1, (self.x-person_type1.get_size()[0]/2, self.y-person_type1.get_size()[1]/2))

    def draw_bg(self, screen):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(750, 0, 250, 750))
        if self.slide == 1:
            screen.blit(narrator, (125,50))
            self.draw_message(screen, "welcome to minidungeon! ")
        elif self.slide == 2:
            screen.blit(narrator, (125,50))
            self.draw_message(screen, "minidungeon is an endless dungeon crawler game where you will need to fight enemies and earn some loot along the way! ")
        elif self.slide == 3:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Use WASD or arrow keys to move. Try it yourself! ")
        elif self.slide == 4:
            self.draw_game_bg(screen)
            self.draw_message(screen, "You may enter through a door by going near it and pressing %s when given the prompt. " % pygame.key.name(CONTROL_CONFIRM[0]))
        elif self.slide == 5:
            self.draw_game_bg(screen)
            self.draw_message(screen, "You cannot travel past the 5x5 grid, nor can you open a door when there are enemies currently in the room with you. ")
        elif self.slide == 6:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Notice that you have a 5x5 minimap on your screen! This will serve as your guide in the game. ")
        elif self.slide == 7:
            self.draw_game_bg(screen)
            self.draw_message(screen, "A red dot = a battle room, a yellow dot = a loot room, a pink dot = a minigame room, and a purple dot = a boss room. ")
        elif self.slide == 8:
            self.draw_game_bg(screen)
            self.draw_message(screen, "The number of these rooms are randomized; however, there will only be one boss room. ")
        elif self.slide == 9:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Battle rooms contain a random number of enemies that will start chasing you and will attack when they are close enough. ")
        elif self.slide == 10:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Press Left-Click on your mouse to attack; note that there is a cooldown to attacks. ")
        elif self.slide == 11:
            self.draw_game_bg(screen)
            self.draw_message(screen, "Loot rooms contain three choices of loot by random chance, and you may select one choice using %s when you are near the black square. " % pygame.key.name(CONTROL_CONFIRM[0]))
        elif self.slide == 12:
            self.draw_game_bg(screen)
            self.draw_message(screen, "In minigame rooms, you can wager 5 coins for the chance to win 10 coins in a random minigame! (find out later!)")
        elif self.slide == 13:
            self.draw_game_bg(screen)
            self.draw_message(screen, "The boss room contains a high-hp boss that will spawn a random number of enemies every once and a while, and you must kill the boss to enter the next stage. ")
        elif self.slide == 14:
            self.map[self.roomx][self.roomy].type = -1
            self.draw_game_bg(screen)
            self.draw_message(screen, "After each successful boss fight, you will be placed into a shop where you can buy things using gold. ")
        elif self.slide == 15:
            screen.blit(narrator, (125,50))
            self.draw_message(screen, "If you run out of lives, you will be placed into the game over screen, where you can then return to the main menu. ")
        elif self.slide == 16:
            screen.blit(narrator, (125,50))
            self.draw_message(screen, "And that's it! You may now go back to the main menu. (or is it ...?)")

# credits screen
class Credits:
    def __init__(self):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)
        self.text = pygame.font.SysFont('Calibri', 24)

    def button_animation(self, screen):
        for _ in range(2):
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 550, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(200+i, 550+i, 600-2*i, 100-2*i))
                screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
                pygame.display.flip()
                pygame.time.wait(20)
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 550, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(210-i, 560-i, 580+2*i, 80+2*i))
                screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
                pygame.display.flip()
                pygame.time.wait(20)
        pygame.event.clear()

    def draw_bg(self, screen):
        screen.blit(self.my_font.render("credits!", True, (0,0,0)), (400,150))
        screen.blit(self.text.render("a work-in-progress game made by Eric Ning", True, (0,0,0)), (275,250))
        screen.blit(self.text.render("expected completion date to be by the end of August 2025", True, (0,0,0)), (200,275))

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 550, 600, 100))
        screen.blit(self.my_font.render("return to main menu?", True, (0,0,0)), (220, 570))
        screen.blit(arrow_default, (80,560))
        screen.blit(arrow_2_default, (820,560))

# achievements screen
class Achievements:
    def __init__(self, unlocked_1, unlocked_2):
        self.screen = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT))
        self.option = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Calibri', 64)
        self.small_font = pygame.font.SysFont('Calibri', 44)
        self.text = pygame.font.SysFont('Calibri', 32)

        self.unlocked_1 = unlocked_1
        self.unlocked_2 = unlocked_2

        self.buttons = ["----------------------------", "----------------------------", "return to main menu?"]
        self.locations = [180, 180, 220] # x coordinates of text

        if unlocked_1:
            self.buttons[0] = "reached the end..?"
            self.locations[0] = 200
        
        if unlocked_2:
            self.buttons[1] = "reached the (true) end"
            self.locations[1] = 170

    def button_animation(self, screen):
        for _ in range(2):
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 600, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(200+i, 600+i, 600-2*i, 100-2*i))
                screen.blit(self.my_font.render(self.buttons[2], True, (0,0,0)), (self.locations[2], 620))
                pygame.display.flip()
                pygame.time.wait(20)
            for i in range(10):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(200, 600, 600, 100))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(210-i, 610-i, 580+2*i, 80+2*i))
                screen.blit(self.my_font.render(self.buttons[2], True, (0,0,0)), (self.locations[2], 620))
                pygame.display.flip()
                pygame.time.wait(20)
        pygame.event.clear()

    def draw_bg(self, screen):
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(725, 250, 250, 250))
        screen.blit(self.my_font.render("your achievements!", True, (0,0,0)), (240,125))
        
        for i in range(2):
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(140, 250+150*i, 450, 100))
            screen.blit(self.small_font.render(self.buttons[i], True, (0,0,0)), (self.locations[i], 280+150*i))
        
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(200, 600, 600, 100))
        screen.blit(self.my_font.render(self.buttons[2], True, (0,0,0)), (self.locations[2], 620))

        if self.option <= 1:
            screen.blit(arrow_default, (20,260+self.option*150))
            screen.blit(arrow_2_default, (610,260+self.option*150))
        else:
            screen.blit(arrow_default, (80,310+self.option*150))
            screen.blit(arrow_2_default, (820,310+self.option*150))

        # achievement descriptions
        if self.option == 0:
            if self.unlocked_1:
                screen.blit(self.text.render("are you really ..", True, (0,0,0)), (760,280))
                screen.blit(self.text.render("truly free?", True, (0,0,0)), (780,330))
                screen.blit(background_slime_2, (800,380))
            else:
                screen.blit(self.text.render("[?????]", True, (0,0,0)), (800,300))
        elif self.option == 1:
            if self.unlocked_2:
                screen.blit(self.text.render("... you finally ..", True, (0,0,0)), (750,395))
                screen.blit(self.text.render("escaped ... :D", True, (0,0,0)), (775,445))
                screen.blit(background_slime_1, (800,270))
            else:
                screen.blit(self.text.render("[?????]", True, (0,0,0)), (800,300))



