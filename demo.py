import pygame
import sys
from settings import *
from player import Player
from gardener import Gardener
from sun import Sun
pygame.init()


SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1
SPAWN_SUN_EVENT = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1400)
pygame.time.set_timer(SPAWN_SUN_EVENT, 2200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Growing Plant")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

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
game_over = False
score = 0

# --------------------
# MAIN LOOP
# --------------------
while True:
    dt = clock.tick(FPS)

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
            g = Gardener()
            obstacles.add(g)
            all_sprites.add(g)

        if event.type == SPAWN_SUN_EVENT and not game_over:
            s = Sun()
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
    screen.fill((30, 30, 40))
    all_sprites.draw(screen)
    player.draw_growth_bar(screen) 
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if player.invincible:
        grow_text = font.render("GROWING!", True, (255, 200, 0))
        screen.blit(grow_text, (WIDTH // 2 - 60, 10))

    if game_over:
        over_text = font.render("GAME OVER - Press R to Restart", True, (255, 80, 80))
        screen.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2))

    pygame.display.flip()
