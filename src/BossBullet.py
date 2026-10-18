import pygame
import math
import random

class BossBulletBase(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.x_float = float(x)
        self.y_float = float(y)
        self.speed_x = float(speed_x)
        self.speed_y = float(speed_y)
    def update(self):
        self.x_float += self.speed_x
        self.y_float += self.speed_y
        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)
        if self.rect.top > 750 or self.rect.bottom < 0 or self.rect.left > 800 or self.rect.right < 0:
            self.kill()

class Boss1_Bullet(BossBulletBase):
    image_cache = {} 
    
    # THÊM BIẾN xoay_anh=False VÀO ĐÂY
    def __init__(self, x, y, speed_x, speed_y, loaidan='dai', xoay_anh=False): 
        if loaidan not in Boss1_Bullet.image_cache:
            if loaidan == 'dai':
                img = pygame.image.load("asset/image/ui/danboss1v2.png").convert_alpha()
                Boss1_Bullet.image_cache['dai'] = pygame.transform.scale(img, (37, 80))
            elif loaidan == 'tron':
                img = pygame.image.load("asset/image/ui/dantron.png").convert_alpha()
                Boss1_Bullet.image_cache['tron'] = pygame.transform.scale(img, (38, 38))
                
        image_goc = Boss1_Bullet.image_cache[loaidan]
        if xoay_anh:
            goc_radian = math.atan2(-speed_y, speed_x)
            goc_do = math.degrees(goc_radian)
            goc_xoay = goc_do - 90 
            image_cuoi = pygame.transform.rotate(image_goc, goc_xoay)
        else:
            image_cuoi = image_goc
        super().__init__(x, y, speed_x, speed_y, image_cuoi)

    @classmethod
    def basic_attack(cls, x, y):
        # Không truyền xoay_anh, mặc định là False
        return [cls(x, y, 0, 5, loaidan='dai')]

    @classmethod
    def special_attack1(cls, x, y):
        return [
            cls(x, y, -3, 6, loaidan='dai'),
            cls(x, y, 0, 6, loaidan='dai'),  
            cls(x, y, 3, 6, loaidan='dai')   
        ]

    @classmethod
    def special_attack2(cls, x, y, so_luong_dan=9, toc_do=4):
        bullets = []
        if so_luong_dan <= 1:
            return [cls(x, y, 0, toc_do, loaidan='tron')]
        goc_chia = 180 / (so_luong_dan - 1)
        for i in range(so_luong_dan):
            goc_hien_tai = i * goc_chia
            radian = math.radians(goc_hien_tai)
            speed_x = math.cos(radian) * toc_do
            speed_y = math.sin(radian) * toc_do
            bullets.append(cls(x, y, speed_x, speed_y, loaidan='tron'))
        return bullets
class Boss2_Bullet(BossBulletBase):
    # THÊM BIẾN xoay_anh=False VÀO ĐÂY
    def __init__(self, x, y, speed_x, speed_y, loaidan='dai', xoay_anh=False): 
        if loaidan not in Boss2_Bullet.image_cache:
            if loaidan == 'dai':
                img = pygame.image.load("asset/image/ui/danboss1v2.png").convert_alpha()
                Boss2_Bullet.image_cache['dai'] = pygame.transform.scale(img, (37, 80))
            elif loaidan == 'tron':
                img = pygame.image.load("asset/image/ui/dantron.png").convert_alpha()
                Boss2_Bullet.image_cache['tron'] = pygame.transform.scale(img, (38, 38))
                
        image_goc = Boss2_Bullet.image_cache[loaidan]
        if xoay_anh:
            goc_radian = math.atan2(-speed_y, speed_x)
            goc_do = math.degrees(goc_radian)
            goc_xoay = goc_do - 90 
            image_cuoi = pygame.transform.rotate(image_goc, goc_xoay)
        else:
            image_cuoi = image_goc
        super().__init__(x, y, speed_x, speed_y, image_cuoi)
    @classmethod
    def basic_attack(cls, x, y):
            # Không truyền xoay_anh, mặc định là False
            return [cls(x, y, 0, 5, loaidan='dai')]
    image_cache = {} 
    @classmethod
    def special_attack1(cls, x, y, chieu_rong=200, loaidan='dai'): 
            bullets = []
            toa_do_x = [x - 100, x , x + 100]
            for i in range(3):
                if i==1:
                   bullets.append(cls(toa_do_x[i], y, speed_x=-3, speed_y=5, loaidan=loaidan, xoay_anh=True)) 
                   bullets.append(cls(toa_do_x[i], y, speed_x=3,  speed_y=5, loaidan=loaidan, xoay_anh=True)) 
                else: 
                    bullets.append(cls(toa_do_x[i], y-50, speed_x=-3, speed_y=5, loaidan=loaidan, xoay_anh=True)) 
                    bullets.append(cls(toa_do_x[i], y-50, speed_x=3,  speed_y=5, loaidan=loaidan, xoay_anh=True))
            return bullets
    @classmethod
    def special_attack2(cls, x, y, player_x, player_y, toc_do=6, loaidan='dai'):
            """Bắn đạn nhắm thẳng vào tọa độ của mục tiêu (người chơi)"""
            dx = player_x - x
            dy = player_y - y
            
            # 2. Tính góc bay (Radian)
            radian = math.atan2(dy, dx)
            
            # 3. Tính vận tốc x, y
            speed_x = math.cos(radian) * toc_do
            speed_y = math.sin(radian) * toc_do
            return [cls(x, y, speed_x, speed_y, loaidan=loaidan, xoay_anh=True)]

boss_bullet_list = [Boss1_Bullet,Boss2_Bullet]