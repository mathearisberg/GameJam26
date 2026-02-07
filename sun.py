import pygame
import random
from settings import *

class Sun(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 30
        self.rect.y = random.randint(50, HEIGHT - 100)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

