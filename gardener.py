import pygame
import os
from PIL import Image
from settings import *

def load_gif_frame(path, size=None):
    gif = Image.open(path)
    frame = gif.convert("RGBA")
    if size:
        frame = frame.resize(size, Image.LANCZOS)
    return pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

class Gardener(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

        gif_path = os.path.join("images", "gartnerGIF.gif")  
   
        width, height = 40, 80
        self.image = load_gif_frame(gif_path, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 40
        self.rect.bottom = HEIGHT

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
