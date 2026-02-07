import pygame
from settings import *
# --------------------
# SPRITES
# --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_size = BASE_SIZE
        self.size = self.base_size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((50, 200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = PLAYER_X
        self.rect.centery = HEIGHT // 2

        self.vel_y = 0
        self.invincible = False
        self.invincible_end = 0

    def jump(self):
        self.vel_y = JUMP_STRENGTH

    def grow(self):
        self.invincible = True
        self.invincible_end = pygame.time.get_ticks() + INVINCIBLE_TIME
        self.size = int(self.base_size * GROWTH_SCALE)

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 220, 100))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def shrink(self):
        self.invincible = False
        self.size = self.base_size
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((50, 200, 50))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.shrink()
