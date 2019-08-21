import pygame, sys
from pygame.locals import *
from lib import enemies, heroes, items
from grid import *
import random
from key_events import KeyEvents
import math

# INSTANCES OF GAME OBJECTS
PLAYER = heroes.PIKACHU()
key_events = KeyEvents(PLAYER)
WAND = items.WAND()
GOLD = items.GOLD()
SWORD = items.SWORD()
SHIELD = items.SHIELD()
BOW = items.BOW()
MEWTWO = enemies.MEWTWO()
PORTAL = enemies.PORTAL()
TEMPLE = TEMPLE()
CHANSEY = heroes.CHANSEY()

# GROUPINGS OF RELATED GAME OBJECTS
GAME_ITEMS = [WAND, SWORD, SHIELD]
GAME_WEAPONS = [WAND, BOW]
KOFFING_LIST = []
orbs_list = []

# OTHER CONFIG
INVFONT = pygame.font.SysFont('FreeSansBold.ttf', 20)
HEALTHFONT = pygame.font.SysFont('FreeSansBold.ttf', 40)
portal_path = './textures/portal/portal_'
portal_images = [portal_path + str(p) + '.png' for p in range(1, 7)]

"""
TIMED EVENTS
"""
# PIKACHU MOVEMENT
pygame.time.set_timer(USEREVENT, 400)
# SPAWN KOFFING
pygame.time.set_timer(USEREVENT + 1, 7500)
# INCREMENT KOFFING PORTAL FRAMES
pygame.time.set_timer(USEREVENT + 2, 400)
# MOVE KOFFING
pygame.time.set_timer(USEREVENT + 3, 1000)
# ORB TRAVEL ON PATH
pygame.time.set_timer(USEREVENT + 4, 100)

GAME_OVER = False
# GAME LOOP
while not GAME_OVER:

    MEWTWO_VULNERABLE_IF = [koffing for koffing in KOFFING_LIST if koffing.APPEAR == True]

    if len(MEWTWO_VULNERABLE_IF) < 1:
        MEWTWO.VULNERABLE = True
    else:
        MEWTWO.VULNERABLE = False

    for event in pygame.event.get():

        keys = pygame.key.get_pressed()
        key_events.global_events()
    
        if event.type == QUIT:
            key_events.quit()
    
        if keys[K_w] and keys[K_t]:
            key_events.key_w()

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
    
        # PLACING DOWN ITEMS
        if (keys[K_SPACE]):
            key_events.key_space()
    
        # FIRE ORB FROM WAND
        if (keys[K_f]):
            if PLAYER.WEAPON == WAND:
                orbs_list.append(heroes.ORB(math.ceil(PLAYER.PLAYER_POS[0]), math.ceil(PLAYER.PLAYER_POS[1]), PLAYER.DIRECTION))

        """
        TIMED EVENTS
        """

        # MEWTWO W/PORTAL MOVEMENT
        if (event.type == USEREVENT):
            if PORTAL.FRAME < 5:
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

       # KOFFING W/PORTAL GENERATOR 
        elif (event.type == USEREVENT + 2):
            for koffing in KOFFING_LIST:
                if koffing.PORTAL_APPEAR and koffing.PORTAL.FRAME < 5:
                    koffing.PORTAL.FRAME += 1
                elif not koffing.SUMMONED:
                    koffing.PORTAL_APPEAR = False
                    koffing.APPEAR = True
                    koffing.SUMMONED = True
                    koffing.POS = [koffing.PORTAL.POS[0], koffing.PORTAL.POS[1]]
        
        # KOFFINGS MOVEMENTS HUNT PLAYER
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
        
        # ORB PATH MOVEMENT ANIMATION
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

        # PICKUP ITEM CONDITIONS
        for item in GAME_ITEMS:
            if PLAYER.PLAYER_POS == item.POS and item.PLACED:
                PLAYER.PLAYER_INV.append(item)
                item.PLACED = False
                if item in GAME_WEAPONS:
                    PLAYER.WEAPON = item

    """
    RENDERING GRID, SPRITES, AND VIEWS
    """

    # RENDER GAME GRID
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURFACE.blit(TEXTURES[GRID[row][column]], (column*TILESIZE, row*TILESIZE))

    # RENDER PIKACHU
    if PLAYER.TRANSFORM:
        DISPLAYSURFACE.blit(PLAYER.WOLF, (PLAYER.PLAYER_POS[0]*TILESIZE, PLAYER.PLAYER_POS[1]*TILESIZE))
    else:
        DISPLAYSURFACE.blit(PLAYER.SPRITE_POS, (PLAYER.PLAYER_POS[0]*TILESIZE, PLAYER.PLAYER_POS[1]*TILESIZE))

    # RENDER TEMPLE
    DISPLAYSURFACE.blit(TEMPLE.SPRITE, (TEMPLE.X_POS*TILESIZE, TEMPLE.Y_POS*TILESIZE))

    # RENDER CHANSEY
    CHANSEY.APPEARED = True
    if CHANSEY.APPEARED:
        if PLAYER.TRANSFORM:
            DISPLAYSURFACE.blit(CHANSEY.SPRITE_POS, (PLAYER.PLAYER_POS[0]*TILESIZE + 20, PLAYER.PLAYER_POS[1] * TILESIZE + 35))
        else:
            DISPLAYSURFACE.blit(CHANSEY.SPRITE_POS, (TEMPLE.X_POS*TILESIZE, TEMPLE.Y_POS*TILESIZE))

    # RENDERING ARMED ITEMS WITH PLAYER SPRITE
    if PLAYER.WEAPON:
        DISPLAYSURFACE.blit(PLAYER.WEAPON.IMAGE_ARMED, (PLAYER.PLAYER_POS[0]*TILESIZE, PLAYER.PLAYER_POS[1]*TILESIZE))

    # RENDER KOFFINGS AND PORTAL
    for koffing in KOFFING_LIST:
        if koffing.PORTAL_APPEAR:
            DISPLAYSURFACE.blit(pygame.image.load(portal_images[koffing.PORTAL.FRAME]), (koffing.PORTAL.POS[0]*TILESIZE, koffing.PORTAL.POS[1]*TILESIZE))
        if koffing.APPEAR:
            DISPLAYSURFACE.blit(koffing.KOFFING, (koffing.POS[0]*TILESIZE, koffing.POS[1]*TILESIZE))

    # RENDER ITEMS
    for item in GAME_ITEMS:
            if item.PLACED == True:
                DISPLAYSURFACE.blit(item.IMAGE, (item.POS[0]*TILESIZE, item.POS[1]*TILESIZE))

    # RENDER ORBS
    for orb in orbs_list:
        if orb.POS == MEWTWO.MEWTWO_POS and MEWTWO.VULNERABLE:
            print('MEWTWO HEALTH', MEWTWO.HEALTH)
            MEWTWO.HEALTH -= 10
        for koffing in KOFFING_LIST:
                if orb.POS == koffing.POS:
                    koffing.APPEAR = False
                    KOFFING_LIST.remove(koffing)
                    orbs_list.remove(orb)
        if orb.POS[0] > MAPWIDTH or orb.POS[0] < 0 or orb.POS[1] > MAPHEIGHT or orb.POS[1] < 0: 
            orbs_list.remove(orb)

        DISPLAYSURFACE.blit(orb.IMAGE, (orb.POS[0]*TILESIZE, orb.POS[1]*TILESIZE))

    # RENDER PLAYER INVENTORY
    INVENTORY_POSITION = 250
    for item in PLAYER.PLAYER_INV:
        DISPLAYSURFACE.blit(item.IMAGE, (INVENTORY_POSITION, MAPHEIGHT*TILESIZE+35))
        INVENTORY_POSITION += 10 
        INVENTORY_TEXT = INVFONT.render(item.NAME, True, WHITE, BLACK)
        DISPLAYSURFACE.blit(INVENTORY_TEXT, (INVENTORY_POSITION, MAPHEIGHT*TILESIZE+15))
        INVENTORY_POSITION += 100

    # RENDER PLAYER HEALTH BAR
    PLAYER_HEALTH_BAR_TEXT = HEALTHFONT.render('PIKACHU HEALTH: ', True, GREEN, BLACK)
    DISPLAYSURFACE.blit(PLAYER_HEALTH_BAR_TEXT, (15, MAPHEIGHT*TILESIZE-500))
    DISPLAYSURFACE.blit(HEALTHFONT.render(str(PLAYER.HEALTH), True, GREEN, BLACK), (225, MAPHEIGHT*TILESIZE - 500))

    # RENDER MEWTWO HEALTH BAR
    PLAYER_MANA_BAR_TEXT = HEALTHFONT.render('MEWTWO HEALTH: ', True, RED, BLACK)
    DISPLAYSURFACE.blit(PLAYER_MANA_BAR_TEXT, (650, MAPHEIGHT*TILESIZE-500))
    DISPLAYSURFACE.blit(HEALTHFONT.render(str(MEWTWO.HEALTH), True, RED, BLACK), (900, MAPHEIGHT*TILESIZE-500))

    # RENDER TREES
    for tree in sorted(trees, key=lambda t: t.Y_POS):
        DISPLAYSURFACE.blit(tree.SPRITE, (tree.X_POS, tree.Y_POS))

    # RENDER MEWTWO AND PORTAL
    DISPLAYSURFACE.blit(pygame.image.load(portal_images[PORTAL.FRAME]), (MEWTWO.MEWTWO_POS[0]*TILESIZE, MEWTWO.MEWTWO_POS[1]*TILESIZE))
    DISPLAYSURFACE.blit(MEWTWO.MEWTWO, (MEWTWO.MEWTWO_POS[0]*TILESIZE, MEWTWO.MEWTWO_POS[1]*TILESIZE))

    
    pygame.display.update()

    if MEWTWO.HEALTH <= 0:
        GAME_OVER = True
        print('GAME OVER, YOU WIN!')
    
    if PLAYER.HEALTH <= 0:
        GAME_OVER = True
        print('GAME OVER, YOU LOSE')

# END OF GAME LOOP


