import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60
ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Decent.io: Tactical Domination")
clock = pygame.time.Clock()

# Load Assets
grass_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
water_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
mountain_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
grass_tile.fill(GREEN)
water_tile.fill(BLUE)
mountain_tile.fill(WHITE)

# Terrain Data
terrain_data = {
    "grass": {"movement_cost": 1, "cover": 0},
    "water": {"movement_cost": 3, "cover": 0},
    "mountain": {"movement_cost": 2, "cover": 25}
}

# Unit Class
class Unit(pygame.sprite.Sprite):
    def __init__(self, type, health, attack, position, player, movement_range=3, action_points=2):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED if player == 1 else YELLOW)
        self.rect = self.image.get_rect(topleft=position)
        self.health = health
        self.max_health = health
        self.attack = attack
        self.player = player
        self.movement_range = movement_range
        self.action_points = action_points
        self.attack_type = "melee" if type == "soldier" else "ranged"

    def move(self, dx, dy):
    new_x, new_y = self.rect.x + dx * TILE_SIZE, self.rect.y + dy * TILE_SIZE

    # Boundary check for game_map
    if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
        row_index = new_y // TILE_SIZE
        col_index = new_x // TILE_SIZE

        # Additional boundary check for accessing game_map
        if 0 <= row_index < len(game_map) and 0 <= col_index < len(game_map[0]): 
            tile_type = game_map[row_index][col_index]
            if tile_type != "water":
                movement_cost = terrain_data[tile_type]["movement_cost"]
                if movement_cost <= self.action_points:
                    self.rect.x = new_x
                    self.rect.y = new_y
                    self.action_points -= movement_cost


    def attack(self, target):
        if self.attack_type == "melee" and self.rect.colliderect(target.rect):
            damage = self.attack - terrain_data[game_map[target.rect.y // TILE_SIZE][target.rect.x // TILE_SIZE]]["cover"]
            target.health -= max(0, damage)
        elif self.attack_type == "ranged" and is_within_attack_range(self, target):
            target.health -= max(0, self.attack)

def is_within_attack_range(attacker, target):
    distance = max(abs(attacker.rect.x - target.rect.x), abs(attacker.rect.y - target.rect.y))
    attack_range = 1 if attacker.attack_type == "melee" else 3
    return distance <= attack_range * TILE_SIZE

# Function to highlight possible moves
def highlight_possible_moves(unit):
    for dx in range(-unit.movement_range, unit.movement_range + 1):
        for dy in range(-unit.movement_range, unit.movement_range + 1):
            new_x, new_y = unit.rect.x + dx * TILE_SIZE, unit.rect.y + dy * TILE_SIZE
            if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
                tile_type = game_map[new_y // TILE_SIZE][new_x // TILE_SIZE]
                movement_cost = terrain_data[tile_type]["movement_cost"]
                if movement_cost <= unit.action_points:
                    pygame.draw.rect(screen, BLUE, (new_x, new_y, TILE_SIZE, TILE_SIZE), 2)

def switch_turn():
    global turn
    turn = 3 - turn
    for unit in units:
        if unit.player == turn:
            unit.action_points = 2

# Fog of War Update
def update_fog_of_war():
    for unit in units:
        if unit.player == 1:
            for dx in range(-unit.movement_range, unit.movement_range + 1):
                for dy in range(-unit.movement_range, unit.movement_range + 1):
                    new_x = (unit.rect.x // TILE_SIZE) + dx
                    new_y = (unit.rect.y // TILE_SIZE) + dy

                    # Boundary check for fog_of_war
                    if 0 <= new_x < len(fog_of_war[0]) and 0 <= new_y < len(fog_of_war):
                        fog_of_war[new_y][new_x] = False

# AI Move Logic
def ai_move():
    for unit in units:
        if unit.player == 2:
            closest_player_unit = min(
                [u for u in units if u.player == 1], 
                key=lambda u: abs(u.rect.x - unit.rect.x) + abs(u.rect.y - unit.rect.y)
            )
            if is_within_attack_range(unit, closest_player_unit):
                unit.attack(closest_player_unit)
                if closest_player_unit.health <= 0:
                    units.remove(closest_player_unit)
                unit.action_points = 0
            else:
                dx = 1 if closest_player_unit.rect.x > unit.rect.x else -1
                dy = 1 if closest_player_unit.rect.y > unit.rect.y else -1
                unit.move(dx, dy)

# UI Rendering
def draw_ui():
    font = pygame.font.Font(None, 36)
    turn_text = f"Player {turn}'s Turn"
    text = font.render(turn_text, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 200, 10))

    if selected_unit:
        stats_text = f"{selected_unit.player} HP: {selected_unit.health}/{selected_unit.max_health} AP: {selected_unit.action_points}"
        stats_render = font.render(stats_text, True, WHITE)
        screen.blit(stats_render, (10, 10))

# Map Rendering
def draw_map():
    screen.fill(BLACK)
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if not fog_of_war[y][x]:
                image = grass_tile if tile == "grass" else water_tile if tile == "water" else mountain_tile
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))
            else:
                pygame.draw.rect(screen, (0, 0, 0, 128), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Units Rendering
def draw_units():
    for unit in units:
        screen.blit(unit.image, unit.rect)
        health_bar_width = unit.health / unit.max_health * TILE_SIZE
        health_bar_rect = pygame.Rect(unit.rect.x, unit.rect.y - 8, health_bar_width, 4)
        pygame.draw.rect(screen, GREEN, health_bar_rect)

        font = pygame.font.Font(None, 20)
        ap_text = font.render(str(unit.action_points), True, WHITE)
        screen.blit(ap_text, (unit.rect.x + TILE_SIZE - 10, unit.rect.y - 10))

# Game Setup
def generate_map(use_perlin=False):
    return [[random.choice(["grass", "grass", "water", "mountain"]) for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]

game_map = generate_map()
fog_of_war = [[True for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]
units = pygame.sprite.Group()
units.add(Unit("soldier", 100, 10, (5 * TILE_SIZE, 5 * TILE_SIZE), 1))
units.add(Unit("robot", 100, 15, (45 * TILE_SIZE, 25 * TILE_SIZE), 2))
turn = 1
selected_unit = None

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for unit in units:
                    if unit.rect.collidepoint(event.pos):
                        if unit.player == turn:
                            selected_unit = unit
                        elif selected_unit and selected_unit.player == turn and is_within_attack_range(selected_unit, unit):
                            selected_unit.attack(unit)
                            if unit.health <= 0:
                                units.remove(unit)
                            selected_unit.action_points = 0
                        elif event.type == pygame.MOUSEBUTTONDOWN and selected_unit:
                            if event.button == 3:  # Right-click to end turn or move
                                if selected_unit.action_points > 0:
                                # Attempt to move the unit to the clicked tile
                                    target_x, target_y = event.pos
                                    dx = (target_x // TILE_SIZE) - (selected_unit.rect.x // TILE_SIZE)
                                    dy = (target_y // TILE_SIZE) - (selected_unit.rect.y // TILE_SIZE)
                                    selected_unit.move(dx, dy)
                    else:
                        switch_turn()

                        break
        if event.type == pygame.KEYDOWN:
            if selected_unit and selected_unit.player == turn:
                if event.key == pygame.K_w:
                    selected_unit.move(0, -1) 
                elif event.key == pygame.K_s:
                    selected_unit.move(0, 1)  
                elif event.key == pygame.K_a:
                    selected_unit.move(-1, 0) 
                elif event.key == pygame.K_d:
                    selected_unit.move(1, 0)   
                elif event.key == pygame.K_SPACE:  # End turn with spacebar
                    switch_turn()

            elif event.button == 3 and selected_unit:
                if selected_unit.action_points > 0:
                    target_x, target_y = event.pos
                    dx = (target_x // TILE_SIZE) - (selected_unit.rect.x // TILE_SIZE)
                    dy = (target_y // TILE_SIZE) - (selected_unit.rect.y // TILE_SIZE)
                    selected_unit.move(dx, dy)
                else:
                    switch_turn()

        if event.type == pygame.KEYDOWN:
            if selected_unit and selected_unit.player == turn:
                if event.key == pygame.K_w:
                    selected_unit.move(0, -1) 
                elif event.key == pygame.K_s:
                    selected_unit.move(0, 1)  
                elif event.key == pygame.K_a:
                    selected_unit.move(-1, 0) 
                elif event.key == pygame.K_d:
                    selected_unit.move(1, 0)

    # AI Turn
    if turn == 2:
        ai_move()  # AI performs its actions
        switch_turn()

    # Update the fog of war based on unit positions
    update_fog_of_war()

    # Draw the game map and units
    draw_map()
    draw_units()

    # Draw the UI elements such as the turn indicator and unit stats
    draw_ui()

    # Highlight the selected unit and its possible movement options
    if selected_unit:
        pygame.draw.rect(screen, YELLOW, selected_unit.rect, 2)
        highlight_possible_moves(selected_unit)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()