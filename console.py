import pygame
import sys
import os
import random

from settings import *
from player import Player
from gardener import Gardener
from sun import Sun
from bird import Bird

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/backgorund_sound_when_playing.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

death_sound = pygame.mixer.Sound("sounds/when_you_die.mp3")

sun_sound = pygame.mixer.Sound("sounds/hitting_the_sun.mp3")

jump_sound = pygame.mixer.Sound("sounds/jumping.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growing Plant")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

background = pygame.image.load(
    os.path.join(BASE_DIR, "images", "hage1.jpg")
).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ground_image = pygame.image.load(
    os.path.join(BASE_DIR, "images", "ground.png")
).convert_alpha()
ground_height = ground_image.get_height()
ground_image = pygame.transform.scale(ground_image, (WIDTH, ground_height))
ground_x = 0


SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1
SPAWN_SUN_EVENT = pygame.USEREVENT + 2
SPAWN_BIRD_EVENT = pygame.USEREVENT + 3

pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1400)
pygame.time.set_timer(SPAWN_SUN_EVENT, 2200)
pygame.time.set_timer(SPAWN_BIRD_EVENT, 2000)

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
suns = pygame.sprite.Group()
birds = pygame.sprite.Group()


def can_spawn_at_right_edge(groups, min_gap):
    for group in groups:
        for sprite in group:
            if abs(sprite.rect.x - WIDTH) < min_gap:
                return False
    return True

def reset_game():
    all_sprites.empty()
    obstacles.empty()
    suns.empty()
    birds.empty()

    player = Player()
    all_sprites.add(player)

    return player


player = reset_game()
game_time = 0
current_speed = BASE_SPEED
difficulty_ratio = 0
game_over = False
score = 0


while True:
    dt = clock.tick(FPS)

    if not game_over:
        game_time += dt
        current_speed = min(
            BASE_SPEED + game_time * SPEED_INCREASE_RATE,
            MAX_SPEED
        )

        difficulty_ratio = (current_speed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED)
        difficulty_ratio = max(0, min(difficulty_ratio, 1))

        ground_x -= current_speed
        if ground_x <= -WIDTH:
            ground_x = 0

        
        keys = pygame.key.get_pressed()
        player.set_crouch(keys[pygame.K_DOWN])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
                jump_sound.play()

            if event.key == pygame.K_r and game_over:
                player = reset_game()
                game_time = 0
                current_speed = BASE_SPEED
                difficulty_ratio = 0
                game_over = False
                score = 0
                ground_x = 0
                pygame.mixer.music.play(-1)


        if event.type == SPAWN_OBSTACLE_EVENT and not game_over:
            chance = SPAWN_DIFFICULTY_START + difficulty_ratio * (
                SPAWN_DIFFICULTY_END - SPAWN_DIFFICULTY_START
            )
            if random.random() < chance:
                if can_spawn_at_right_edge([obstacles, birds], MIN_HORIZONTAL_GAP):
                    g = Gardener(current_speed)
                    obstacles.add(g)
                    all_sprites.add(g)

        if event.type == SPAWN_SUN_EVENT and not game_over:
            if random.random() < max(0.15, 0.6 - difficulty_ratio * 0.4):
                s = Sun(current_speed)
                suns.add(s)
                all_sprites.add(s)

        if event.type == SPAWN_BIRD_EVENT and not game_over:
            if random.random() < 0.3 + difficulty_ratio * 0.5:
                if can_spawn_at_right_edge([obstacles, birds], MIN_HORIZONTAL_GAP):
                    b = Bird(current_speed * 1.1)
                    birds.add(b)
                    all_sprites.add(b)

    if not game_over:
        all_sprites.update()
        score += 1

        if pygame.sprite.spritecollide(player, suns, True):
            player.grow()
            sun_sound.play()

        if pygame.sprite.spritecollide(player, obstacles, False):
            if player.invincible:
                pygame.sprite.spritecollide(player, obstacles, True)
            else:
                game_over = True
                death_sound.play()
                pygame.mixer.music.stop()

        if pygame.sprite.spritecollide(player, birds, False):
            if player.invincible:
                pygame.sprite.spritecollide(player, birds, True)
            else:
                game_over = True
                death_sound.play()
                pygame.mixer.music.stop()
                


    screen.blit(background, (0, 0))
    screen.blit(ground_image, (ground_x, HEIGHT - ground_height))
    screen.blit(ground_image, (ground_x + WIDTH, HEIGHT - ground_height))
    all_sprites.draw(screen)

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

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
