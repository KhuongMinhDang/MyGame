import pygame
import random
from src.BossBullet import boss_bullet_list
from src.Boss_time import boss_time_list

class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_id=0):
        super().__init__()
        self.boss_id = boss_id
        #them anh boss vo day
        self.image_boss = [
            pygame.image.load('asset/image/SpaceShips/boss1v2.png').convert_alpha()
        ]
        
        self.image = self.image_boss[self.boss_id]
        self.image = pygame.transform.scale(self.image, (289, 216))
        self.rect = self.image.get_rect(midtop=(400, -200))
        if self.boss_id==0: self.hp=1000
        self.bullets = pygame.sprite.Group() # Nhóm chứa đạn của boss này
        self.dang_bay = True
        self.speed_x = 0
        self.speed_y = 4
        self.move_timer = pygame.time.get_ticks() 
        self.co_che=boss_time_list[self.boss_id](self)
    def luong_mau(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
    def update(self):
        now = pygame.time.get_ticks()
        #dang nhoai manf hinh
        if self.dang_bay:
            self.rect.y += self.speed_y
            if self.rect.y >= 20:
                self.rect.y = 20
                self.dang_bay = False 
                self.speed_x = random.choice([-3, 3])        
        #luc vao man hinh
        else:
            if self.boss_id == 0:
                self.rect.x += self.speed_x
                if self.rect.left <= 0:
                    self.rect.left = 0
                    self.speed_x = random.randint(2, 4) 
                elif self.rect.right >= 800: 
                    self.rect.right = 800
                    self.speed_x = random.randint(-4, -2) 
                    
                if now - self.move_timer > 2000: 
                    self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])
                    self.move_timer = now
                self.co_che.update(now)#luc ban dan
