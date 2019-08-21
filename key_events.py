import pygame
import sys

# IMAGES FOR PIKACHU MOVEMENTS

img_path = './sprites/pikachu/pikachu_'
f_path = img_path + 'f'
b_path = img_path + 'b'
r_path = img_path + 'r'
l_path = img_path + 'l'

f_images = [f_path+str(f)+'.png' for f in range(1)]
b_images = [b_path+str(b)+'.png' for b in range(1)]
r_images = [r_path+str(r)+'.png' for r in range(1)] 
l_images = [l_path+str(l)+'.png' for l in range(1)]

# IMAGES FOR RAICHU ANIMATED WALKING

img_path = './sprites/raichu/raichu_'
raichu_f_path = img_path + 'f'
raichu_b_path = img_path + 'b'
raichu_r_path = img_path + 'r'
raichu_l_path = img_path + 'l'

raichu_f_images = [raichu_f_path + str(f) + '.png' for f in range(7)]
raichu_b_images = [raichu_b_path + str(b) + '.png' for b in range(7)]
raichu_r_images = [raichu_r_path + str(r) + '.png' for r in range(4)]
raichu_l_images = [raichu_l_path + str(l) + '.png' for l in range(4)]

class KeyEvents:
    def __init__(self, PLAYER):
        self.PLAYER = PLAYER
        self.counter = 0
        self.raichu_counter = 0
        self.raichu_counter_lr = 0
        self.movement = .25
        self.orbs = []

    def global_events(self):
        if self.PLAYER.TRANSFORM:
            self.movement =  .5
        else:
            self.movement = .25

    def quit(self):
        pygame.quit()
        sys.exit()

    def key_down(self):
        self.PLAYER.PLAYER_POS[1] += self.movement
        self.PLAYER.DIRECTION = 'd'

        self.PLAYER.SPRITE_POS = pygame.image.load(f_images[self.counter])
        self.counter = (self.counter + 1) % len(f_images)

        if self.PLAYER.TRANSFORM:
            self.PLAYER.RAICHU  = pygame.image.load(raichu_f_images[self.raichu_counter])
            self.raichu_counter = (self.raichu_counter + 1) % len(raichu_f_images)

    def key_up(self):
        self.PLAYER.PLAYER_POS[1] -= self.movement 
        self.PLAYER.DIRECTION = 'u'

        self.PLAYER.SPRITE_POS = pygame.image.load(b_images[self.counter])
        self.counter = (self.counter + 1) % len(b_images)

        if self.PLAYER.TRANSFORM:
            self.PLAYER.RAICHU  = pygame.image.load(raichu_b_images[self.raichu_counter])
            self.raichu_counter = (self.raichu_counter + 1) % len(raichu_b_images)

    def key_left(self):
        self.PLAYER.PLAYER_POS[0] -= self.movement 
        self.PLAYER.DIRECTION = 'l'

        self.PLAYER.SPRITE_POS = pygame.image.load(l_images[self.counter])
        self.counter = (self.counter + 1) % len(l_images)

        if self.PLAYER.TRANSFORM:
            self.PLAYER.RAICHU  = pygame.image.load(raichu_l_images[self.raichu_counter_lr])
            self.raichu_counter_lr = (self.raichu_counter_lr + 1) % len(raichu_l_images)

    def key_right(self):
        self.PLAYER.PLAYER_POS[0] += self.movement
        self.PLAYER.DIRECTION = 'r'

        self.PLAYER.SPRITE_POS = pygame.image.load(r_images[self.counter])
        self.counter = (self.counter + 1) % len(r_images)

        if self.PLAYER.TRANSFORM:
            self.PLAYER.RAICHU  = pygame.image.load(raichu_r_images[self.raichu_counter_lr])
            self.raichu_counter_lr = (self.raichu_counter_lr + 1) % len(raichu_r_images)

    def key_space(self):
        if self.PLAYER.WEAPON:
            self.PLAYER.PLAYER_INV.remove(self.PLAYER.WEAPON)
            self.PLAYER.WEAPON.PLACED = True

            # DROP WEAPON LOCATION
            if self.PLAYER.DIRECTION == 'd':
                    self.PLAYER.WEAPON.POS[0] = self.PLAYER.PLAYER_POS[0]
                    self.PLAYER.WEAPON.POS[1] = self.PLAYER.PLAYER_POS[1] - 1
            elif self.PLAYER.DIRECTION == 'u':
                    self.PLAYER.WEAPON.POS[0] = self.PLAYER.PLAYER_POS[0]
                    self.PLAYER.WEAPON.POS[1] = self.PLAYER.PLAYER_POS[1] + 1
            elif self.PLAYER.DIRECTION == 'r':
                    self.PLAYER.WEAPON.POS[0] = self.PLAYER.PLAYER_POS[0] - 1
                    self.PLAYER.WEAPON.POS[1] = self.PLAYER.PLAYER_POS[1]
            elif self.PLAYER.DIRECTION == 'l':
                    self.PLAYER.WEAPON.POS[0] = self.PLAYER.PLAYER_POS[0] + 1
                    self.PLAYER.WEAPON.POS[1] = self.PLAYER.PLAYER_POS[1]

        self.PLAYER.WEAPON = False
    
    def key_w(self):
        self.PLAYER.TRANSFORMING()

