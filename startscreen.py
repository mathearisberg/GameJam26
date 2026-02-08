# startscreen.py
import pygame
import sys
import os
from PIL import Image
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growing Plant")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_gif(path, max_size):
    frames = []
    durations = []

    try:
        pil_gif = Image.open(path)
        while True:
            frame = pil_gif.convert("RGBA")
            duration = pil_gif.info.get("duration", 100)
            durations.append(max(20, int(duration)))

            surf = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )

            w, h = surf.get_size()
            scale = min(max_size / w, max_size / h, 1.0)
            if scale != 1.0:
                surf = pygame.transform.smoothscale(
                    surf, (int(w * scale), int(h * scale))
                )

            frames.append(surf)
            pil_gif.seek(pil_gif.tell() + 1)
    except EOFError:
        pass

    return frames, durations


def show_start_screen():
    start_bg = pygame.image.load(
        os.path.join(BASE_DIR, "images", "hage1.jpg")
    ).convert()
    start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

    button_img = pygame.image.load(
        os.path.join(BASE_DIR, "images", "start-knapp.png")
    ).convert_alpha()
    button_img = pygame.transform.smoothscale(button_img, (240, 150))
    button_rect = button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    title_font = pygame.font.SysFont(None, 64)

    plant_frames, plant_durs = load_gif(
        os.path.join(BASE_DIR, "images", "planteGif.gif"), 220
    )
    gardener_frames, gardener_durs = load_gif(
        os.path.join(BASE_DIR, "images", "gartnerGIF.gif"), 220
    )
    fungus_frames, fungus_durs = load_gif(
        os.path.join(BASE_DIR, "images", "fung.gif"), 160
    )

    pi = gi = fi = 0
    pa = ga = fa = 0

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    running = False

        screen.blit(start_bg, (0, 0))

        title = title_font.render("Growing Plant", True, (255, 255, 255))
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4)
        )

        screen.blit(button_img, button_rect)

        if plant_frames:
            pa += dt
            if pa >= plant_durs[pi]:
                pa = 0
                pi = (pi + 1) % len(plant_frames)
            f = plant_frames[pi]
            screen.blit(
                f,
                (button_rect.left - f.get_width() - 20,
                 button_rect.centery - f.get_height() // 2)
            )

        if gardener_frames:
            ga += dt
            if ga >= gardener_durs[gi]:
                ga = 0
                gi = (gi + 1) % len(gardener_frames)
            f = gardener_frames[gi]
            screen.blit(
                f,
                (button_rect.right + 20,
                 button_rect.centery - f.get_height() // 2)
            )

        if fungus_frames:
            fa += dt
            if fa >= fungus_durs[fi]:
                fa = 0
                fi = (fi + 1) % len(fungus_frames)
            f = fungus_frames[fi]
            screen.blit(f, (WIDTH - f.get_width() - 20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    show_start_screen()

    # Import here to avoid circular init issues
    from demo import run_game
    run_game()
