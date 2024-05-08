# monster.py

import pygame
import random

# monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.direction = random.choice([-1, 1])  # Start moving left or right
        self.starting_x = self.rect.x  

    def update(self):
        self.rect.x += 5 * self.direction  # Move at a set speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Change direction at screen edges
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))  # Stay in bounds

        # Keep the monster within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
