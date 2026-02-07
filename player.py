import pygame
import os
from PIL import Image
from settings import *


def load_gif_frames(path, size):
    gif = Image.open(path)
    frames = []

    try:
        while True:
            frame = gif.convert("RGBA")
            frame = frame.resize(size, Image.LANCZOS)

            pygame_image = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            frames.append(pygame_image)

            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Slightly bigger base player size
        self.normal_width = int(BASE_WIDTH * 2.25)
        self.normal_height = int(BASE_HEIGHT * 2.25)
        self.grown_scale = 1.8

        # ---- Load GIF frames ----
        gif_path = os.path.join("images", "planteGif.gif")
        self.frames = load_gif_frames(
            gif_path,
            (self.normal_width, self.normal_height)
        )

        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 0.15  # lower = faster animation

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = PLAYER_X
        self.rect.centery = HEIGHT // 2

        self.vel_y = 0

        self.reset_state()

    def reset_state(self):
        self.is_grown = False
        self.invincible = False

        self.max_jumps = 3
        self.jumps_left = self.max_jumps
        self.jump_strength = JUMP_STRENGTH

    def jump(self):
        if self.jumps_left > 0:
            self.vel_y = self.jump_strength * 1.15
            self.jumps_left -= 1

    def grow(self):
        self.is_grown = True
        self.invincible = True
        self.invincible_end = pygame.time.get_ticks() + INVINCIBLE_TIME

        self.max_jumps = 1
        self.jumps_left = 1
        self.jump_strength = JUMP_STRENGTH * 0.5

        # Scale frames
        w = int(self.normal_width * self.grown_scale)
        h = int(self.normal_height * self.grown_scale)

        gif_path = os.path.join("images", "planteGif.gif")
        self.frames = load_gif_frames(gif_path, (w, h))

        center = self.rect.center
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)

    def shrink(self):
        gif_path = os.path.join("images", "planteGif.gif")
        self.frames = load_gif_frames(
            gif_path,
            (self.normal_width, self.normal_height)
        )

        center = self.rect.center
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)

        self.reset_state()

    def update(self):
        # ---- Animate GIF ----
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.jumps_left = self.max_jumps

        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.invincible = False
            self.is_grown = False
            self.shrink()