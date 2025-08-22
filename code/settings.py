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

bg_default = pygame.image.load(os.path.join("images", "bg_default.png"))
arrow_default = pygame.image.load(os.path.join("images", "arrow_default.png"))
person_default = pygame.image.load(os.path.join("images", "person_default.png"))
enemy_default = pygame.image.load(os.path.join("images", "enemy_default.png"))
portal_default = pygame.image.load(os.path.join("images", "portal_default.png"))

enemy_slime = pygame.image.load(os.path.join("images", "enemy_slime.png"))
archer_slime = pygame.image.load(os.path.join("images", "archer_slime.png"))
boss_slime = pygame.image.load(os.path.join("images", "boss_slime.png"))
projectile = pygame.image.load(os.path.join("images", "projectile.png"))
person_type1 = pygame.image.load(os.path.join("images", "person_type1.png"))
narrator = pygame.image.load(os.path.join("images", "narrator.png"))
background_slime_1 = pygame.image.load(os.path.join("images", "background_slime_1.png"))
background_slime_2 = pygame.image.load(os.path.join("images", "background_slime_2.png"))