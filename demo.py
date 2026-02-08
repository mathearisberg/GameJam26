import pygame
import sys
import os
import random

from settings import *
from player import Player
from gardener import Gardener
from sun import Sun
from bird import Bird

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Growing Plant")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

# --------------------
# ASSETS
# --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background = pygame.image.load(
    os.path.join(BASE_DIR, "images", "hage1.jpg")
).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# --------------------
# EVENTS
# --------------------
SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1
SPAWN_SUN_EVENT = pygame.USEREVENT + 2
SPAWN_BIRD_EVENT = pygame.USEREVENT + 3

pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1400)
pygame.time.set_timer(SPAWN_SUN_EVENT, 2200)
pygame.time.set_timer(SPAWN_BIRD_EVENT, 2000)

# --------------------
# GROUPS
# --------------------
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
suns = pygame.sprite.Group()
birds = pygame.sprite.Group()

# --------------------
# GAME SETUP
# --------------------
def reset_game():
    all_sprites.empty()
    obstacles.empty()
    suns.empty()
    birds.empty()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(BASE_DIR, "images", "hage1.jpg")


    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load ground image
    ground_path = os.path.join(BASE_DIR, "images", "ground.png")
    ground_image = pygame.image.load(ground_path).convert_alpha()

    # Scale ground to screen width, keep its height
    ground_height = ground_image.get_height()
    ground_image = pygame.transform.scale(ground_image, (WIDTH, ground_height))

    # Ground scrolling
    ground_x = 0
    GROUND_SCROLL_SPEED = BASE_SPEED



    SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1
    SPAWN_SUN_EVENT = pygame.USEREVENT + 2

    pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1400)
    pygame.time.set_timer(SPAWN_SUN_EVENT, 2200)


    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    suns = pygame.sprite.Group()


def can_spawn_at_right_edge(groups, min_gap):
    for group in groups:
        for sprite in group:
            if abs(sprite.rect.x - WIDTH) < min_gap:
                return False
    return True


player = reset_game()

game_time = 0
current_speed = BASE_SPEED
difficulty_ratio = 0
game_over = False
score = 0

# --------------------
# MAIN LOOP
# --------------------
while True:
    dt = clock.tick(FPS)

    # ---- GAME PROGRESSION ----
    if not game_over:
        game_time += dt
        current_speed = min(
            BASE_SPEED + game_time * SPEED_INCREASE_RATE,
            MAX_SPEED
        )
        difficulty_ratio = (current_speed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED)
        difficulty_ratio = max(0, min(difficulty_ratio, 1))

        # crouch = hold DOWN
        keys = pygame.key.get_pressed()
        player.set_crouch(keys[pygame.K_DOWN])

    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()

            if event.key == pygame.K_r and game_over:
                player = reset_game()
                game_time = 0
                current_speed = BASE_SPEED
                difficulty_ratio = 0
                game_over = False
                score = 0

        # ---- GARDENER ----
        if event.type == SPAWN_OBSTACLE_EVENT and not game_over:
            spawn_chance = (
                SPAWN_DIFFICULTY_START +
                difficulty_ratio * (SPAWN_DIFFICULTY_END - SPAWN_DIFFICULTY_START)
            )

            if random.random() < spawn_chance:
                if can_spawn_at_right_edge([birds, obstacles], MIN_HORIZONTAL_GAP):
                    g = Gardener(current_speed)
                    obstacles.add(g)
                    all_sprites.add(g)

        # ---- SUN ----
        if event.type == SPAWN_SUN_EVENT and not game_over:
            sun_chance = max(0.15, 0.6 - difficulty_ratio * 0.4)

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

        # ---- BIRD ----
        if event.type == SPAWN_BIRD_EVENT and not game_over:
            bird_chance = 0.3 + difficulty_ratio * 0.5

            if random.random() < bird_chance:
                if can_spawn_at_right_edge([obstacles, birds], MIN_HORIZONTAL_GAP):
                    b = Bird(current_speed * 1.1)
                    birds.add(b)
                    all_sprites.add(b)

    # ---- UPDATE ----
    if not game_over:
        all_sprites.update()
        score += 1
    player = reset_game()
    game_time = 0
    current_speed = BASE_SPEED
    game_over = False
    score = 0

    difficulty_ratio = (current_speed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED)
    difficulty_ratio = max(0, min(difficulty_ratio, 1))

        if pygame.sprite.spritecollide(player, obstacles, False):
            if player.invincible:
                pygame.sprite.spritecollide(player, obstacles, True)
            else:
                game_over = True

        if pygame.sprite.spritecollide(player, birds, False):
            if player.invincible:
                pygame.sprite.spritecollide(player, birds, True)
            else:
                game_over = True

    # ---- DRAW ----
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    screen.blit(
        font.render(f"Score: {score}", True, (255, 255, 255)),
        (10, 10)
    )

    if player.invincible:
        screen.blit(
            font.render("GROWING!", True, (255, 200, 0)),
            (WIDTH // 2 - 60, 10)
        )

    if game_over:
        screen.blit(
            font.render("GAME OVER - Press R to Restart", True, (255, 80, 80)),
            (WIDTH // 2 - 160, HEIGHT // 2)
        )

    pygame.display.flip()

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
            # Scroll ground
            ground_x -= current_speed
            if ground_x <= -WIDTH:
                ground_x = 0

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

                    # Reset speed scaling so a new run starts slow again
                    game_time = 0
                    current_speed = BASE_SPEED
                    difficulty_ratio = 0

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
        # Draw scrolling ground (tiled)
        screen.blit(ground_image, (ground_x, HEIGHT - ground_height))
        screen.blit(ground_image, (ground_x + WIDTH, HEIGHT - ground_height))
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
