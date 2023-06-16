# weapon.py

import pygame

# Weapon class
class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, color):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self):
        # Follow the mouse cursor
        self.rect.center = pygame.mouse.get_pos()
