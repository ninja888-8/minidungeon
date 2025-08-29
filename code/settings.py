import pygame
import os

WINDOW_LENGTH = 1000
WINDOW_HEIGHT = 750
BG = (173, 216, 230)

# colours of large squares
VISITED = (152, 251, 152)
CURRENT = (247, 244, 141)
UNKNOWN = (144, 150, 144)

# colours of adjacent squares
UNKNOWN_BOSS = (145, 98, 166)
UNKNOWN_GAME = (255, 179, 246)
UNKNOWN_LOOT = (236, 247, 22)
UNKNOWN_BATTLE = (252, 99, 91)

# controls
CONTROL_U = (pygame.K_w, pygame.K_UP)
CONTROL_D = (pygame.K_s, pygame.K_DOWN)
CONTROL_L = (pygame.K_a, pygame.K_LEFT)
CONTROL_R = (pygame.K_d, pygame.K_RIGHT)
CONTROL_CONFIRM = (pygame.K_e, pygame.K_RETURN)

#default
bg_default = pygame.image.load(os.path.join("images", "bg_default.png"))
arrow_default = pygame.image.load(os.path.join("images", "arrow_default.png"))
arrow_2_default = pygame.image.load(os.path.join("images", "arrow_2_default.png"))
person_default = pygame.image.load(os.path.join("images", "person_default.png"))
enemy_default = pygame.image.load(os.path.join("images", "enemy_default.png"))
portal_default = pygame.image.load(os.path.join("images", "portal_default.png"))

#enemies
enemy_slime = pygame.image.load(os.path.join("images", "enemy_slime.png"))
enemy_slime_tank = pygame.image.load(os.path.join("images", "enemy_slime_tank.png"))
archer_slime = pygame.image.load(os.path.join("images", "archer_slime.png"))
boss_slime = pygame.image.load(os.path.join("images", "boss_slime.png"))
projectile = pygame.image.load(os.path.join("images", "projectile.png"))

#characters
person_type1 = pygame.image.load(os.path.join("images", "person_type1.png"))
narrator = pygame.image.load(os.path.join("images", "narrator.png"))

#icons
background_slime_1 = pygame.image.load(os.path.join("images", "background_slime_1.png"))
background_slime_2 = pygame.image.load(os.path.join("images", "background_slime_2.png"))
gain_atk = pygame.image.load(os.path.join("images", "gain_atk.png"))
gain_def = pygame.image.load(os.path.join("images", "gain_def.png"))
gain_gold = pygame.image.load(os.path.join("images", "gain_gold.png"))
gain_life = pygame.image.load(os.path.join("images", "gain_life.png"))
gain_range = pygame.image.load(os.path.join("images", "gain_range.png"))

#backdrops
bg_boss = pygame.image.load(os.path.join("images", "bg_boss.png"))
bg_battle = pygame.image.load(os.path.join("images", "bg_battle.png"))
bg_default_2 = pygame.image.load(os.path.join("images", "bg_default_2.png"))