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

        # --- Sizes ---
        self.normal_size = (int(BASE_WIDTH), int(BASE_HEIGHT))
        self.crouch_size = (int(BASE_WIDTH), int(CROUCH_HEIGHT))
        self.grown_scale = 1.8

        # --- State ---
        self.is_crouching = False
        self.is_grown = False
        self.invincible = False

        # --- Load animations ---
        self.normal_frames = load_gif_frames(
            os.path.join("images", "planteGif.gif"),
            self.normal_size
        )
        self.crouch_frames = load_gif_frames(
            os.path.join("images", "litenPlante.gif"),
            self.crouch_size
        )

        self.frames = self.normal_frames
        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 0.15

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = PLAYER_X
        self.rect.centery = HEIGHT // 2

        # --- Physics ---
        self.vel_y = 0

        self.reset_state()

    # --------------------
    # STATE
    # --------------------
    def reset_state(self):
        self.is_grown = False
        self.invincible = False

        self.max_jumps = 3
        self.jumps_left = self.max_jumps
        self.jump_strength = JUMP_STRENGTH

    # --------------------
    # ACTIONS
    # --------------------
    def jump(self):
        if self.is_crouching:
            return
        if self.jumps_left > 0:
            self.vel_y = self.jump_strength * 1.15
            self.jumps_left -= 1

    def grow(self):
        self.is_grown = True
        self.invincible = True
        self.invincible_end = pygame.time.get_ticks() + INVINCIBLE_TIME

        # force uncrouch
        self.is_crouching = False

        self.max_jumps = 1
        self.jumps_left = 1
        self.jump_strength = JUMP_STRENGTH * 0.5

        w = int(BASE_WIDTH * self.grown_scale)
        h = int(BASE_HEIGHT * self.grown_scale)

        grown_frames = load_gif_frames(
            os.path.join("images", "planteGif.gif"),
            (w, h)
        )

        self._set_frames(grown_frames)

    def shrink(self):
        self._set_frames(self.normal_frames)
        self.reset_state()

    # --------------------
    # UPDATE
    # --------------------
    def update(self):
        # --- Animate ---
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # --- Gravity ---
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # --- Bounds ---
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.jumps_left = self.max_jumps

        # --- Invincibility timeout ---
        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.invincible = False
            self.is_grown = False
            self.shrink()

    # --------------------
    # CROUCH
    # --------------------
    def set_crouch(self, crouching: bool):
        if crouching == self.is_crouching:
            return

        if self.is_grown:
            return

        bottom = self.rect.bottom

        if crouching:
            self._set_frames(self.crouch_frames)
        else:
            self._set_frames(self.normal_frames)

        self.is_crouching = crouching
        self.rect.bottom = bottom

    # --------------------
    # INTERNAL
    # --------------------
    def _set_frames(self, frames):
        center = self.rect.center
        self.frames = frames
        self.frame_index = 0
        self.frame_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)
