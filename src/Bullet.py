import pygame
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.image = pygame.Surface((10,15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=player.rect.midtop)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < -10:
            self.kill()