import pygame
from map_generator import generate_map

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tactical.io")
clock = pygame.time.Clock()

# Load Assets (Replace with your own assets)
grass_tile = pygame.image.load("assets/grass.png").convert_alpha()
water_tile = pygame.image.load("assets/water.png").convert_alpha()
mountain_tile = pygame.image.load("assets/mountain.png").convert_alpha()
soldier_img = pygame.image.load("assets/soldier.png").convert_alpha()
robot_img = pygame.image.load("assets/robot.png").convert_alpha()

# Terrain Types (Movement Costs and Cover)
terrain_data = {
    "grass": {"movement_cost": 1, "cover": 0},
    "water": {"movement_cost": 3, "cover": 0},
    "mountain": {"movement_cost": 2, "cover": 25}  # Example cover percentage
}

# Unit Class
class Unit(pygame.sprite.Sprite):
    def __init__(self, type, health, attack, position, player, movement_range=3, action_points=2):
        super().__init__()
        self.image = soldier_img if type == "soldier" else robot_img
        self.rect = self.image.get_rect(topleft=position)
        self.health = health
        self.attack = attack
        self.player = player
        self.movement_range = movement_range
        self.action_points = action_points
        self.attack_type = "melee" if type == "soldier" else "ranged"

    def move(self, dx, dy):
        if self.action_points > 0:
            self.rect.x += dx * TILE_SIZE
            self.rect.y += dy * TILE_SIZE
            self.action_points -= 1

    def attack(self, target):
        if self.action_points > 0:
            target.health -= self.attack
            if target.health <= 0:
                target.kill()
            self.action_points -= 1

    def use_skill(self, skill):
        # Define skill logic here
        print(f"Using skill: {skill}")

    def use_item(self, item):
        # Define item usage logic here
        print(f"Using item: {item}")

# Game State
game_map = generate_map(use_perlin=True)
units = pygame.sprite.Group()
resources = {"energy": 100, "materials": 50}
players = {"player1": 1, "AI": 2}
turn = 1
selected_unit = None
fog_of_war = [[True for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]

# Create Starting Units
units.add(Unit("soldier", 100, 10, (5 * TILE_SIZE, 5 * TILE_SIZE), players["player1"]))
units.add(Unit("robot", 100, 15, (45 * TILE_SIZE, 25 * TILE_SIZE), players["AI"]))

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle User Input
        if event.type == pygame.MOUSEBUTTONDOWN:
            for unit in units:
                if unit.rect.collidepoint(event.pos):
                    selected_unit = unit
                    break
        if event.type == pygame.KEYDOWN:
            if selected_unit:
                if event.key == pygame.K_w:
                    selected_unit.move(0, -1)  # Move up
                elif event.key == pygame.K_s:
                    selected_unit.move(0, 1)   # Move down
                elif event.key == pygame.K_a:
                    selected_unit.move(-1, 0)  # Move left
                elif event.key == pygame.K_d:
                    selected_unit.move(1, 0)   # Move right
                elif event.key == pygame.K_SPACE:
                    for unit in units:
                        if unit != selected_unit and unit.player != selected_unit.player:
                            if selected_unit.rect.colliderect(unit.rect):
                                selected_unit.attack(unit)
                elif event.key == pygame.K_q:
                    selected_unit.use_skill("Skill 1")
                elif event.key == pygame.K_e:
                    selected_unit.use_skill("Skill 2")
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                    item_number = event.key - pygame.K_0
                    selected_unit.use_item(f"Item {item_number}")

    # Game Logic
    # Check for victory conditions, resource updates, and fog of war
    for unit in units:
        if unit.health <= 0:
            unit.kill()

    # Rendering
    screen.fill((0, 0, 0))  
    # Draw Map (with fog of war applied)
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if not fog_of_war[y][x]:  # Only reveal explored tiles
                image = grass_tile if tile == "grass" else water_tile if tile == "water" else mountain_tile
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw Units
    for unit in units:
        screen.blit(unit.image, unit.rect)
        # Draw health bar
        health_bar_width = int((unit.health / 100) * unit.rect.width)
        pygame.draw.rect(screen, (255, 0, 0), (unit.rect.x, unit.rect.y - 10, unit.rect.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (unit.rect.x, unit.rect.y - 10, health_bar_width, 5))

    # Draw UI (resources, turn indicator, etc.)
    font = pygame.font.Font(None, 36)
    energy_text = font.render(f'Energy: {resources["energy"]}', True, (255, 255, 255))
    materials_text = font.render(f'Materials: {resources["materials"]}', True, (255, 255, 255))
    turn_text = font.render(f'Turn: {"Player" if turn == 1 else "AI"}', True, (255, 255, 255))
    screen.blit(energy_text, (10, 10))
    screen.blit(materials_text, (10, 50))
    screen.blit(turn_text, (10, 90))

    # Highlight Selected Unit (If any)
    if selected_unit:
        pygame.draw.rect(screen, (255, 255, 0), selected_unit.rect, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
