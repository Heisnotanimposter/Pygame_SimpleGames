import pygame
from pygamerpg import pygamerpg
from pygameracing import pygameracing

class MainPlatform:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.current_game = None  # Store the active game

        # Create instances of the games
        self.pygamedealmeter = PygameDealmeter(self.screen)
        self.pygameracersparadise = PygameRacersParadaise(self.screen)

    def run(self):
        self.show_menu()  # Display initial selection menu

    def show_menu(self):
        # ... Code to display a menu with options to start each game... 

    def start_game(self, game_name):
        if game_name == "dealmeter":
            self.current_game = self.pygamedealmeter
        elif game_name == "racersparadise":
            self.current_game = self.pygameracersparadise

        if self.current_game:
            self.current_game.run()  # Start the selected game's loop

platform = MainPlatform()
platform.run() 
