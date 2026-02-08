import pygame
import os
from PIL import Image
from settings import *


def load_gif_frames(path, size=None):
    gif = Image.open(path)
    frames = []

    try:
        while True:
            frame = gif.convert("RGBA")
            if size:
                frame = frame.resize(size, Image.LANCZOS)

            pygame_image = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            frames.append(pygame_image)

            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames


class Bird(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.speed = speed

        self.frames = load_gif_frames(
            os.path.join("images", "fung.gif"),
            (BIRD_WIDTH, BIRD_HEIGHT)
        )

        if not self.frames:
            raise RuntimeError("Bird GIF failed to load")

        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 40
        self.rect.y = BIRD_Y

    def update(self):
        self.frame_timer += self.animation_speed
        
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()
