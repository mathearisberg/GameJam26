import pygame
import random
import os
from settings import *

class Sun(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

        png_path = os.path.join("images", "sun.png") 
        self.image = pygame.image.load(png_path).convert_alpha()  

        
        width, height = 70, 70
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + width
        self.rect.y = random.randint(50, HEIGHT - 100)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
