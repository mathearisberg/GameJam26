# startscreen.py
import pygame
import sys
import os
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

    button_width, button_height = 200, 60
    button_color = (50, 200, 50)
    button_hover = (70, 220, 70)
    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)

    title_font = pygame.font.SysFont(None, 64)
    button_font = pygame.font.SysFont(None, 36)

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

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, button_rect)
            if mouse_pressed:
                running = False  # Gå videre til spillet
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        button_text = button_font.render("PLAY", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                  button_rect.centery - button_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

# ---- Start programmet ----
if __name__ == "__main__":
    show_start_screen()  # Vis startskjerm
    run_game()           # Start demo-spillet når PLAY trykkes
