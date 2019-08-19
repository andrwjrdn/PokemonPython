import pygame
import sys
from pygame.locals import *
from lib import enemies, heroes, items
from grid import *
import random
from key_events import key_events
import math

# OBJECTS FOR GAME

PLAYER = heroes.PIKACHU()
key_events = KeyEvents(Player)
WAND = items.WAND()
GOLD = items.GOLD()
SWORD = items.SWORD()
BOW = items.BOW()
MEWTWO = enemies.MEWTWO()
PORTAL = enemies.PORTAL()
TEMPLE = TEMPLE()
MIDNA = heroes.MIDNA()

# WEAPONS/IN-GAME ITEMS

GAME_ITEMS = [WAND, SWORD, SHIELD]
GAME_WEAPONS = [WAND, BOW]
koffing_LIST = []
orbs_list = []

# TIMER FOR SPECIFIC IN-GAME EVENTS

# MEWTWO MECHANICS/MOVEMENT
pygame.time.set_timer(USEREVENT, 400)
# SPAWN KOFFING
pygame.time.set_timer(USEREVENT + 1, 7500)
# INCREMENT KOFFING PORTAL FRAMES
pygame.time.set_timer(USEREVENT + 2, 400)
# KOFFING MECHANICS/MOVEMENTS
pygame.time.set_timer(USEREVENT + 3, 1000)
# ORB TRAVEL ON PATH
pygame.time.set_timer(USEREVENT + 4, 100)

GAME_OVER = False

# OVERALL GAME MECHANICS/FLOW

while not GAME_OVER:

  MEWTWO_VUNERABLE_IF = [
      koffing for koffing in KOFFING_LIST if koffing.APPEAR == True]

  if len(MEWTWO_VULNERABLE_IF) < 1:
    MEWTWO.VULNERABLE = True
  else:
    MEWTWO.VULNERABLE = False

  for event in pygame.event.get():

    keys = pygame.key.get_pressed()
    key_events.global_events()

    if event.type == QUIT:
      key_events.quit()

# MOVE RIGHT
  if (keys[K_RIGHT]) and PLAYER.PLAYER_POS[0] < MAPWIDTH - 1:
           key_events.key_right()

# MOVE LEFT
  if (keys[K_LEFT]) and PLAYER.PLAYER_POS[0] > 0:
           key_events.key_left()

# MOVE UP
  if (keys[K_UP]) and PLAYER.PLAYER_POS[1] > 0:
            key_events.key_up()

# MOVE DOWN
  if (keys[K_DOWN]) and PLAYER.PLAYER_POS[1] < MAPHEIGHT - 1:
            key_events.key_down()

# PICK UP ITEMS WITH SPACEBAR
if (keys[K_SPACE]):
  key_events.key_space()

# FIRE WEAPON FROM ITEM

if (keys[K_f]):
  if PLAYER.WEAPON == WAND:
      orbs_list.append(heroes.ORB(math.ceil(PLAYER.PLAYER_POS[0]), math.ceil(
          PLAYER.PLAYER_POS[1]), PLAYER.DIRECTION))


# MEWTWO W/ PORTAL MOVEMENT
if (event.type == USEREVENT):
  if PORTAL.FRAME < 5;
      PORTAL.FRAME += 1
  else:
    x = random.randint(1, 9)
    y = random.randint(1, 9)
    PORTAL.POS = [x, y]
    MEWTWO.MEWTWO_POS = [x, y]
    PORTAL.FRAME = 1

# KOFFING OBJECT GENERATOR
elif (event.type == USEREVENT + 1):
  NEW_KOFFING = enemies.KOFFING()
  NEW_KOFFING.PORTAL = enemies.PORTAL()
  KOFFING_LIST.append(NEW_KOFFING)

# KOFFING W/ PORTAL GENERATOR
elif (event.type == USEREVENT + 2):
  for koffing in KOFFING_LIST:
    if koffing.PORTAL_APPEAR and koffing.PORTAL.FRAME < 5:
                    koffing.PORTAL.FRAME += 1
    elif not koffing.SUMMONED:
          koffing.PORTAL_APPEAR = False
          koffing.APPEAR = True
          koffing.SUMMONED = True
          koffing.POS = [koffing.PORTAL.POS[0], koffing.PORTAL.POS[1]]

# KOFFING MOVEMENTS TO DAMAGE PLAYER
elif (event.type == USEREVENT + 3):
            for koffing in KOFFING_LIST:
                if koffing.APPEAR:
                    if PLAYER.PLAYER_POS == koffing.POS:
                        PLAYER.HEALTH -= 10
                    for coordinate in range(len(koffing.POS)):
                        if PLAYER.PLAYER_POS[coordinate] > koffing.POS[coordinate]:
                            koffing.POS[coordinate] += 1
                        else:
                            koffing.POS[coordinate] -= 1

# MOVEMENT OF ORB MECHANICS
elif (event.type == USEREVENT + 4):
            for orb in orbs_list:
                if orb.DIRECTION == 'd':
                    orb.POS[1] += 1
                elif orb.DIRECTION == 'u':
                    orb.POS[1] -= 1
                elif orb.DIRECTION == 'l':
                    orb.POS[0] -= 1
                elif orb.DIRECTION == 'r':
                    orb.POS[0] += 1

# ITEM CONDITIONS
  for item in GAME_ITEMS:
            if PLAYER.PLAYER_POS == item.POS and item.PLACED:
                PLAYER.PLAYER_INV.append(item)
                item.PLACED = False
                if item in GAME_WEAPONS:
                    PLAYER.WEAPON = item

# RENDERING THE GRID FOR GAME

for row in range(MAPHEIGHT):
  for column in range(MAPWIDTH):
      DISPLAYSURFACE.blit(TEXTURES[GRID[row] [column]], (column*TILESIZE, row*TILESIZE))

# RENDER PIKACHU

if PLAYER.TRANSFORM:
    DISPLAYSURFACE.blit(PLAYER.WOLF, (PLAYER.PLAYER_POST[0]*TILESIZE, PLAYER.PLAYER_POS[1]*TILESIZE))
else:
        DISPLAYSURFACE.blit(PLAYER.SPRITE_POS, (PLAYER.PLAYER_POS[0]*TILESIZE, PLAYER.PLAYER_POS[1]*TILESIZE))

# RENDER POKEGYM
DISPLAYSURFACE.blit(TEMPLE.SPRITE, (TEMPLE.X_POS*TILESIZE, TEMPLE.Y_POS*TILESIZE))






