# main.py

import pygame
from sandbag import Sandbag
from weapon import Weapon

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sandbag Punch")

# Colors
BLACK = (0, 0, 0)

# Create sandbag sprite
sandbag = Sandbag(WIDTH, HEIGHT)
all_sprites = pygame.sprite.Group()
all_sprites.add(sandbag)

# Create weapon sprites
weapon_sprites = pygame.sprite.Group()
weapons = [
    ("sword", (255, 0, 0)),
    ("gun", (0, 255, 0)),
    ("bomb", (0, 0, 255))
]
for weapon_name, weapon_color in weapons:
    weapon = Weapon(weapon_name, weapon_color)
    weapon_sprites.add(weapon)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    weapon_sprites.update()

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    weapon_sprites.draw(screen)
    pygame.display.flip()

# Quit the game
pygame.quit()
