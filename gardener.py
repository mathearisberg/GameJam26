import pygame
from settings import *
class Gardener(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill((200, 60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 40
        self.rect.bottom = HEIGHT
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()