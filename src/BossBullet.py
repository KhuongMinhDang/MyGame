import pygame
class BossBulletBase(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > 750 or self.rect.bottom < 0 or self.rect.left > 800 or self.rect.right < 0:
            self.kill()
class Boss1_Bullet(BossBulletBase):
    image_cache = None # Bộ nhớ đệm ảnh
    def __init__(self, x, y, speed_x, speed_y):
        if Boss1_Bullet.image_cache is None:
            img = pygame.image.load("asset/image/ui/danboss1v2.png").convert_alpha()
            Boss1_Bullet.image_cache = pygame.transform.scale(img, (37, 80))
        super().__init__(x, y, speed_x, speed_y, Boss1_Bullet.image_cache)
    @classmethod
    def basic_attack(cls, x, y):
        return [cls(x, y, 0, 5)]
    @classmethod
    def special_attack(cls, x, y):
        return [
            cls(x, y, -3, 6),
            cls(x, y, 0, 6),  
            cls(x, y, 3, 6)   
        ]
boss_bullet_list = [Boss1_Bullet]