import pygame.image
from grid import MAPHEIGHT, MAPWIDTH
import random

rand = random.randint

class MEWTWO:
    def __init__(self):
        self.MEWTWO = pygame.image.load('./sprites/mewtwo.png')
        self.MEWTWO_POS = [rand(0, MAPWIDTH-1), rand(0, MAPHEIGHT-1)]
        self.HEALTH = 250
        self.VULNERABLE = True

class KOFFING:
    def __init__(self):
        self.KOFFING = pygame.image.load('./sprites/koffing.png')
        self.PORTAL = False
        self.PORTAL_APPEAR = True
        self.APPEAR = False 
        self.POS = []
        self.SUMMONED = False
        self.HEALTH = 100

class PORTAL:
    def __init__(self):
        self.PORTAL = pygame.image.load('./textures/portal/portal_1.png')
        self.POS = [rand(0, MAPWIDTH-1), rand(0, MAPHEIGHT-1)]
        self.FRAME = 0