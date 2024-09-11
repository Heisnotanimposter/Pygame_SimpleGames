import pygame
from map_generator import generate_map
import random
# Initialize Pygame
pygame.init()

# Constants
ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
WIDTH = COLUMNS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
TILE_SIZE = 100
RADIUS = int(SQUARESIZE / 2)

terrain_data = {
    "grass": {"movement_cost": 1, "cover": 0},
    "water": {"movement_cost": 3, "cover": 0},
    "mountain": {"movement_cost": 2, "cover": 25} 
}
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")

# Game Logic
turn = 0
selected_unit = None

# Main Game Loop
def main():
    game = ConnectFour()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx / SQUARESIZE)

                    if game.drop_piece(col):
                        if game.check_winner() == 1:
                            label = "Player 1 Wins!"
                            game_over = True
                        turn += 1
                        turn = turn % 2

                else:
                    # Placeholder for AI or player 2 logic
                    pass

                # Call draw_board function to update the display
                draw_board(game.board)

                if game_over:
                    pygame.time.wait(3000)

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

if __name__ == "__main__":
    main()
