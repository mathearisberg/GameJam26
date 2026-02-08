# startscreen.py
import pygame
import sys
import os
from PIL import Image
from demo import run_game  # <-- Importer funksjonen
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growing Plant")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def show_start_screen():
    start_bg_path = os.path.join(BASE_DIR, "images", "hage1.jpg")
    start_bg = pygame.image.load(start_bg_path).convert()
    start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

    button_img_path = os.path.join(BASE_DIR, "images", "start-knapp.png")
    button_img = pygame.image.load(button_img_path).convert_alpha()

    # Make the start button small and clean
    BUTTON_WIDTH = 240
    BUTTON_HEIGHT = 150
    button_img = pygame.transform.smoothscale(
        button_img, (BUTTON_WIDTH, BUTTON_HEIGHT)
    )

    button_rect = button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    title_font = pygame.font.SysFont(None, 64)

    # ---- Load and prepare animated plant GIF (Pillow -> pygame surfaces) ----
    gif_path = os.path.join(BASE_DIR, "images", "planteGif.gif")
    gif_frames = []
    gif_durations_ms = []

    try:
        pil_gif = Image.open(gif_path)
        # Extract all frames
        while True:
            frame = pil_gif.convert("RGBA")
            duration = pil_gif.info.get("duration", 100)  # ms per frame (fallback 100ms)
            gif_durations_ms.append(max(20, int(duration)))  # clamp to avoid 0ms

            # Convert PIL image -> pygame surface
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            surf = pygame.image.fromstring(data, size, mode)

            # Optional: scale GIF if it's too big/small (keep aspect ratio)
            max_w = 220
            max_h = 220
            w, h = surf.get_size()
            scale = min(max_w / w, max_h / h, 1.0)
            if scale != 1.0:
                surf = pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))

            gif_frames.append(surf)

            pil_gif.seek(pil_gif.tell() + 1)
    except EOFError:
        pass  # end of frames
    except Exception as e:
        print(f"Could not load animated GIF '{gif_path}': {e}")

    gif_index = 0
    gif_accum_ms = 0

    # ---- Load gardener GIF (right of button) ----
    gardener_path = os.path.join(BASE_DIR, "images", "gartnerGIF.gif")
    gardener_frames = []
    gardener_durations_ms = []

    try:
        pil_gif = Image.open(gardener_path)
        while True:
            frame = pil_gif.convert("RGBA")
            duration = pil_gif.info.get("duration", 100)
            gardener_durations_ms.append(max(20, int(duration)))

            surf = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

            max_w, max_h = 220, 220
            w, h = surf.get_size()
            scale = min(max_w / w, max_h / h, 1.0)
            if scale != 1.0:
                surf = pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))

            gardener_frames.append(surf)
            pil_gif.seek(pil_gif.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"Could not load gardener GIF: {e}")

    gardener_index = 0
    gardener_accum_ms = 0

    # ---- Load fungus GIF (top-right corner) ----
    fungus_path = os.path.join(BASE_DIR, "images", "fung.gif")
    fungus_frames = []
    fungus_durations_ms = []

    try:
        pil_gif = Image.open(fungus_path)
        while True:
            frame = pil_gif.convert("RGBA")
            duration = pil_gif.info.get("duration", 100)
            fungus_durations_ms.append(max(20, int(duration)))

            surf = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

            max_w, max_h = 160, 160
            w, h = surf.get_size()
            scale = min(max_w / w, max_h / h, 1.0)
            if scale != 1.0:
                surf = pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))

            fungus_frames.append(surf)
            pil_gif.seek(pil_gif.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"Could not load fungus GIF: {e}")

    fungus_index = 0
    fungus_accum_ms = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(start_bg, (0, 0))
        title_text = title_font.render("Growing Plant", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        screen.blit(button_img, button_rect.topleft)

        if button_rect.collidepoint(mouse_pos) and mouse_pressed:
            running = False  # Start game

        dt_ms = clock.get_time()

        # ---- Plant GIF (left of PLAY button) ----
        if gif_frames:
            gif_accum_ms += dt_ms
            dur = gif_durations_ms[gif_index]
            if gif_accum_ms >= dur:
                gif_accum_ms = 0
                gif_index = (gif_index + 1) % len(gif_frames)

            frame = gif_frames[gif_index]
            x = button_rect.left - frame.get_width() - 20
            y = button_rect.centery - frame.get_height() // 2
            screen.blit(frame, (x, y))

        # ---- Gardener GIF (right of PLAY button) ----
        if gardener_frames:
            gardener_accum_ms += dt_ms
            dur = gardener_durations_ms[gardener_index]
            if gardener_accum_ms >= dur:
                gardener_accum_ms = 0
                gardener_index = (gardener_index + 1) % len(gardener_frames)

            frame = gardener_frames[gardener_index]
            x = button_rect.right + 20
            y = button_rect.centery - frame.get_height() // 2
            screen.blit(frame, (x, y))

        # ---- Fungus GIF (top-right corner) ----
        if fungus_frames:
            fungus_accum_ms += dt_ms
            dur = fungus_durations_ms[fungus_index]
            if fungus_accum_ms >= dur:
                fungus_accum_ms = 0
                fungus_index = (fungus_index + 1) % len(fungus_frames)

            frame = fungus_frames[fungus_index]
            x = WIDTH - frame.get_width() - 20
            y = 20
            screen.blit(frame, (x, y))

        pygame.display.flip()
        clock.tick(60)

# ---- Start programmet ----
if __name__ == "__main__":
    show_start_screen()  # Vis startskjerm
    run_game()           # Start demo-spillet når PLAY trykkes