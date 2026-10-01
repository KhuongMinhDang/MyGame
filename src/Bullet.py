import pygame
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < -10:
            self.kill()