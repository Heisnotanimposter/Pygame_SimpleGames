# sandbag.py

import pygame
import random

# Sandbag class
class Sandbag(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        # Move the sandbag randomly
        self.rect.x += random.randint(-5, 5)
        self.rect.y += random.randint(-5, 5)

        # Keep the sandbag within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
