import pygame
import sys
import os

from settings import *
from player import Player
from gardener import Gardener
import random
from sun import Sun


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growing Plant")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(BASE_DIR, "images", "hage1.jpg")

background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1
SPAWN_SUN_EVENT = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1400)
pygame.time.set_timer(SPAWN_SUN_EVENT, 2200)


all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
suns = pygame.sprite.Group()



# --------------------
# GAME SETUP
# --------------------
def reset_game():
    all_sprites.empty()
    obstacles.empty()
    suns.empty()

    player = Player()
    all_sprites.add(player)
    return player


all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
suns = pygame.sprite.Group()

player = reset_game()
game_time = 0
current_speed = BASE_SPEED
game_over = False
score = 0

difficulty_ratio = (current_speed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED)
difficulty_ratio = max(0, min(difficulty_ratio, 1))


# --------------------
# MAIN LOOP
# --------------------
while True:
    dt = clock.tick(FPS)

    if not game_over:
        game_time += dt
        current_speed = min(
            BASE_SPEED + game_time * SPEED_INCREASE_RATE,
            MAX_SPEED
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
            if event.key == pygame.K_r and game_over:
                player = reset_game()
                game_over = False
                score = 0

        if event.type == SPAWN_OBSTACLE_EVENT and not game_over:
            spawn_chance = (
                SPAWN_DIFFICULTY_START +
                difficulty_ratio * (SPAWN_DIFFICULTY_END - SPAWN_DIFFICULTY_START)
            )

            if random.random() < spawn_chance:
                g = Gardener(current_speed)
                obstacles.add(g)
                all_sprites.add(g)


        if event.type == SPAWN_SUN_EVENT and not game_over:
            sun_chance = max(0.15, 0.6 - difficulty_ratio * 0.4)

            if random.random() < sun_chance:
                s = Sun(current_speed)
                suns.add(s)
                all_sprites.add(s)

    if not game_over:
        all_sprites.update()
        score += 1

        if pygame.sprite.spritecollide(player, suns, True):
            player.grow()

        if pygame.sprite.spritecollide(player, obstacles, False):
            if player.invincible:
                for g in pygame.sprite.spritecollide(player, obstacles, True):
                    g.kill()
            else:
                game_over = True

    # --------------------
    # DRAW
    # --------------------
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if player.invincible:
        grow_text = font.render("GROWING!", True, (255, 200, 0))
        screen.blit(grow_text, (WIDTH // 2 - 60, 10))

    if game_over:
        over_text = font.render("GAME OVER - Press R to Restart", True, (255, 80, 80))
        screen.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2))

    pygame.display.flip()
