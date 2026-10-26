import pygame
import math
class BossBulletBase(pygame.sprite.Sprite):
    shared_cache = {} # Dùng chung 1 kho nhớ đệm ảnh cho toàn bộ đạn Boss
    def __init__(self, x, y, speed_x, speed_y, loaidan='dai', xoay_anh=False):
        super().__init__()
        # 1. Load ảnh 1 lần duy nhất
        if loaidan not in BossBulletBase.shared_cache:
            if loaidan == 'dai':
                img = pygame.transform.scale(pygame.image.load("asset/image/ui/danboss1v2.png").convert_alpha(), (37, 80))
            elif loaidan == 'tron':
                img = pygame.transform.scale(pygame.image.load("asset/image/ui/dantron.png").convert_alpha(), (38, 38))
            BossBulletBase.shared_cache[loaidan] = img      
        image_goc = BossBulletBase.shared_cache[loaidan]
        # 2. Xoay đạn
        if xoay_anh:
            goc_do = math.degrees(math.atan2(-speed_y, speed_x))
            self.image = pygame.transform.rotate(image_goc, goc_do - 90)
        else:
            self.image = image_goc
        # 3. Tọa độ & hitbox
        self.rect = self.image.get_rect(center=(x, y))
        self.x_float, self.y_float = float(x), float(y)
        self.speed_x, self.speed_y = float(speed_x), float(speed_y)
        hitbox_size = int(min(image_goc.get_size()) * 0.5)
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center
    def update(self):
        self.x_float += self.speed_x
        self.y_float += self.speed_y
        self.rect.centerx, self.rect.centery = int(self.x_float), int(self.y_float)
        self.hitbox.center = self.rect.center
        if self.rect.top > 750 or self.rect.bottom < 0 or self.rect.left > 800 or self.rect.right < 0:
            self.kill()
    @classmethod
    def basic_attack(cls, x, y):
        """Chiêu bắn thường chung cho mọi Boss"""
        return [cls(x, y, 0, 5, loaidan='dai')]
class Boss1_Bullet(BossBulletBase):
    @classmethod
    def special_attack1(cls, x, y):
        return [cls(x, y, -3, 6, 'dai'), cls(x, y, 0, 6, 'dai'), cls(x, y, 3, 6, 'dai')]
    @classmethod
    def special_attack2(cls, x, y, so_luong_dan=9, toc_do=4):
        if so_luong_dan <= 1: return [cls(x, y, 0, toc_do, 'tron')]
        bullets = []
        for i in range(so_luong_dan):
            rad = math.radians(i * (180 / (so_luong_dan - 1)))
            bullets.append(cls(x, y, math.cos(rad) * toc_do, math.sin(rad) * toc_do, 'tron'))
        return bullets
class Boss2_Bullet(BossBulletBase):
    @classmethod
    def special_attack1(cls, x, y, chieu_rong=200, loaidan='dai'): 
        bullets = []
        for i, tx in enumerate([x - 100, x, x + 100]):
            oy = y if i == 1 else y - 50
            bullets.extend([cls(tx, oy, -3, 5, loaidan, True), cls(tx, oy, 3, 5, loaidan, True)])
        return bullets
    @classmethod
    def special_attack2(cls, x, y, player_x, player_y, toc_do=6, loaidan='dai'):
        rad = math.atan2(player_y - y, player_x - x)
        return [cls(x, y, math.cos(rad) * toc_do, math.sin(rad) * toc_do, loaidan, True)]
class Boss3_Bullet(BossBulletBase):
    goc_xoay_xuan_oc = 0
    @classmethod
    def special_attack1(cls, x, y, so_luong_tia=4, toc_do=5, loaidan='tron'):
        cls.goc_xoay_xuan_oc += 15
        bullets = []
        for i in range(so_luong_tia):
            rad = math.radians(cls.goc_xoay_xuan_oc + i * (360 / so_luong_tia))
            bullets.append(cls(x, y, math.cos(rad) * toc_do, math.sin(rad) * toc_do, loaidan, True))
        return bullets
    @classmethod
    def special_attack2(cls, x, y, so_luong_moi_canh=5, spacing=25, toc_do=6, loaidan='dai'):
        bullets = [cls(x, y, 0, toc_do, loaidan, True)]
        for i in range(1, so_luong_moi_canh):
            offset = i * spacing
            bullets.extend([cls(x - offset, y - offset, 0, toc_do, loaidan, True),
                            cls(x + offset, y - offset, 0, toc_do, loaidan, True)])
        return bullets
boss_bullet_list = [Boss1_Bullet, Boss2_Bullet, Boss3_Bullet]