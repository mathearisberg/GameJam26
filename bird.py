import pygame
import random
from settings import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 0, 0))  # red bird
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH + 50

        # Fixed flight lanes (Google Dino style)
        self.rect.y = BIRD_Y

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
