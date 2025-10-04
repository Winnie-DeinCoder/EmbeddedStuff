import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Dash")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Player
player_size = (50, 50)
player_x = 100
player_y = HEIGHT - player_size[1] - 50
player_vel_y = 0
is_jumping = False
gravity = 1

# Obstacles
obstacle_width = 40
obstacle_height = 40
obstacle_color = (139, 69, 19)  # Brown stone
obstacles = []
obstacle_timer = 0
obstacle_spawn_interval = 1500  # milliseconds

# Score
start_ticks = pygame.time.get_ticks()
game_over = False

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x, y, *player_size))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, obstacle_color, (x, y, obstacle_width, obstacle_height))

def display_text(text, x, y, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def reset_game():
    global obstacles, player_y, is_jumping, player_vel_y, start_ticks, game_over
    obstacles.clear()
    player_y = HEIGHT - player_size[1] - 50
    is_jumping = False
    player_vel_y = 0
    start_ticks = pygame.time.get_ticks()
    game_over = False

# Game loop
while True:
    dt = clock.tick(60)
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = -18
                is_jumping = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    if not game_over:
        # Player physics
        player_y += player_vel_y
        player_vel_y += gravity
        if player_y >= HEIGHT - player_size[1] - 50:
            player_y = HEIGHT - player_size[1] - 50
            is_jumping = False

        # Spawn obstacles
        obstacle_timer += dt
        if obstacle_timer > obstacle_spawn_interval:
            obstacle_x = WIDTH + random.randint(0, 100)
            obstacle_y = HEIGHT - obstacle_height - 50
            obstacles.append([obstacle_x, obstacle_y])
            obstacle_timer = 0

        # Move and draw obstacles
        for obs in obstacles[:]:
            obs[0] -= 7
            draw_obstacle(*obs)

            # Collision
            player_rect = pygame.Rect(player_x, player_y, *player_size)
            obstacle_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
            if player_rect.colliderect(obstacle_rect):
                game_over = True

            # Remove off-screen obstacles
            if obs[0] < -obstacle_width:
                obstacles.remove(obs)

        # Score
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        display_text(f"Score: {seconds}", 10, 10)

        # Draw player
        draw_player(player_x, player_y)

    else:
        display_text("Game Over!", WIDTH // 2 - 120, HEIGHT // 2 - 40)
        display_text("Press 'R' to Restart", WIDTH // 2 - 180, HEIGHT // 2 + 10)

    pygame.display.flip()
