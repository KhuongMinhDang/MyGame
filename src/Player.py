import pygame
class player(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()
        self.image_ship=[
            pygame.image.load('asset/image/SpaceShips/Ship_1.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_2.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_3.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_4.png').convert_alpha()
            ]
        self.image=self.image_ship[x]
        self.rect=self.image.get_rect(center=(400,600))
    def update(self):
        # di chuyen va dieu chinh toa do player
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 5
            if self.rect.left <= 0: self.rect.left = 0
        if key[pygame.K_d]:
            self.rect.x += 5
            if self.rect.right >= 800: self.rect.right = 800
        if key[pygame.K_w]:
            self.rect.y -= 5
            if self.rect.top <= 0: self.rect.top = 0
        if key[pygame.K_s]:
            self.rect.y += 5
            if self.rect.bottom >= 750: self.rect.bottom = 750

