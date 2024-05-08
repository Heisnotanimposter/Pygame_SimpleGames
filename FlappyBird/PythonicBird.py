import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Bird properties
bird = {
    'x': 50,
    'y': screen_height // 2,
    'width': 20,
    'height': 20,
    'velocity': 0,
    'gravity': 0.2,
    'jump_strength': -5
}

# Game variables
pipes = []
score = 0
game_speed = 2
space_between_pipes = 900
pipe_frequency = 100  # Every 100 frames a new pipe will be generated
frame_count = 0

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Font
font = pygame.font.SysFont('Arial', 20)

def create_pipe():
    minHeight = 50
    maxHeight = screen_height - space_between_pipes - minHeight
    topHeight = random.randint(minHeight, maxHeight)
    bottomHeight = screen_height - space_between_pipes - topHeight
    pipe = {
        'x': screen_width,
        'topHeight': topHeight,
        'bottomY': topHeight + space_between_pipes,
        'bottomHeight': bottomHeight,
        'width': 40,
        'passed': False
    }
    pipes.append(pipe)

def draw():
    screen.fill((255, 255, 255))  # Clear screen by filling it with white
    # Draw bird
    pygame.draw.rect(screen, red, (bird['x'], bird['y'], bird['width'], bird['height']))
    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, green, (pipe['x'], 0, pipe['width'], pipe['topHeight']))
        pygame.draw.rect(screen, green, (pipe['x'], pipe['bottomY'], pipe['width'], pipe['bottomHeight']))
    # Draw score
    score_text = font.render('Score: ' + str(score), True, black)
    screen.blit(score_text, (10, 25))

def update():
    global score
    bird['velocity'] += bird['gravity']
    bird['y'] += bird['velocity']
    # Move pipes
    rem = []
    for pipe in pipes:
        pipe['x'] -= game_speed
        # Check for collision
        if (bird['x'] < pipe['x'] + pipe['width'] and
            bird['x'] + bird['width'] > pipe['x'] and
            (bird['y'] < pipe['topHeight'] or bird['y'] + bird['height'] > pipe['bottomY'])):
            gameOver()
        if pipe['x'] + pipe['width'] < bird['x'] and not pipe['passed']:
            pipe['passed'] = True
            score += 1
        if pipe['x'] + pipe['width'] < 0:
            rem.append(pipe)
    for r in rem:
        pipes.remove(r)
    # Check for hitting the ground
    if bird['y'] + bird['height'] > screen_height:
        gameOver()

def gameOver():
    pygame.quit()
    sys.exit()

def resetGame():
    bird['y'] = screen_height // 2
    bird['velocity'] = 0
    global pipes, score, game_speed
    pipes = []
    score = 0
    game_speed = 2

def main_loop():
    global frame_count
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird['velocity'] = bird['jump_strength']
        update()
        draw()
        pygame.display.update()
        frame_count += 1
        if frame_count % pipe_frequency == 0:
            create_pipe()
        pygame.time.Clock().tick(30)  # Set the frame rate to 30 FPS

main_loop()
pygame.quit()
