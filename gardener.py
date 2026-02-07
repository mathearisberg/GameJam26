import pygame
from settings import *
class Gardener(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill((200, 60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 40
        self.rect.bottom = HEIGHT

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()