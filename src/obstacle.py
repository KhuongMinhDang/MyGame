import pygame
from random import randint
import math
class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill(('Red'))
        self.type=type
        self.x0 = randint(25, 775)
        self.y = -5

        self.t = 0
        self.A = 100
        self.speed = 10

        self.rect = self.image.get_rect(center=(self.x0, self.y))
    def update(self):
        if self.type=="sin":
            self.t += 0.05

            self.rect.centerx = self.x0 + self.A * math.sin(self.t)
            self.rect.y += self.speed
        else: self.rect.y +=15

        if self.rect.top >= 750:
            self.kill()
