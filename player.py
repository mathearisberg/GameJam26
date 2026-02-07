import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.normal_width = BASE_WIDTH
        self.normal_height = BASE_HEIGHT
        self.grown_scale = 1.8

        self.reset_state()

        self.rect = self.image.get_rect()
        self.rect.x = PLAYER_X
        self.rect.centery = HEIGHT // 2

        self.vel_y = 0

    def reset_state(self):
        self.is_grown = False
        self.invincible = False

        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.jump_strength = JUMP_STRENGTH

        self.image = pygame.Surface((self.normal_width, self.normal_height))
        self.image.fill((50, 200, 50))

    def jump(self):
        if self.jumps_left > 0:
            self.vel_y = self.jump_strength
            self.jumps_left -= 1

    def grow(self):
        self.is_grown = True
        self.invincible = True
        self.invincible_end = pygame.time.get_ticks() + INVINCIBLE_TIME

        self.max_jumps = 1
        self.jumps_left = 1
        self.jump_strength = JUMP_STRENGTH * 0.5  # small hop

        w = int(self.normal_width * self.grown_scale)
        h = int(self.normal_height * self.grown_scale)

        center = self.rect.center
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 220, 100))
        self.rect = self.image.get_rect(center=center)

    def shrink(self):
        self.reset_state()
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def update(self):
        # gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # ceiling
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        # ground
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.jumps_left = self.max_jumps  # reset jumps

        # invincibility timeout
        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.invincible = False
            self.is_grown = False
            self.shrink()

    def should_tint(self):
        if not self.invincible:
            return False

        time_left = self.invincible_end - pygame.time.get_ticks()
        ratio = time_left / INVINCIBLE_TIME

        # No tinting for first half
        if ratio > 0.5:
            return False

        # Blink faster as time runs out
        blink_speed = int(200 * ratio) + 50  # ms
        return (pygame.time.get_ticks() // blink_speed) % 2 == 0


