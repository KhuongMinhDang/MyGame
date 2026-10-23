import pygame
from src.BossBullet import boss_bullet_list

class Boss1_time:
    def __init__(self, boss):
        self.boss = boss # Nhận vào con Boss để lấy tọa độ và Group đạn
        self.basic_delay = 800
        self.skill_delay1 = 8000
        self.skill_delay2=12000
        self.dan_trong_chuoi= 10
        self.last_basic_shot = pygame.time.get_ticks()
        self.last_skill_shot1 = pygame.time.get_ticks()
        self.last_skill_shot2=pygame.time.get_ticks()
        self.skill=0
        self.bullet_count = 0
        self.last_bullet_time = 0
        self.time_between_bullets = 100
    def update(self, now,player_x,player_y):
        bullet_class = boss_bullet_list[0]
        if self.skill == 0:
            if now - self.last_basic_shot > self.basic_delay:
                new_bullets = bullet_class.basic_attack(self.boss.rect.centerx, self.boss.rect.bottom)
                self.boss.bullets.add(*new_bullets)
                self.last_basic_shot = now
            if now - self.last_skill_shot2 > self.skill_delay2:
                self.skill = 2
                self.bullet_count = 0
            elif now - self.last_skill_shot1 > self.skill_delay1:
                self.skill = 1
                self.bullet_count = 0
        else:
            if now - self.last_bullet_time > self.time_between_bullets:
                if self.skill == 1:
                    new_bullets = bullet_class.special_attack1(self.boss.rect.centerx, self.boss.rect.bottom)
                elif self.skill == 2:
                  new_bullets = bullet_class.special_attack2( self.boss.rect.centerx, self.boss.rect.bottom)
                self.boss.bullets.add(*new_bullets)
                self.bullet_count += 1
                self.last_bullet_time = now
                if self.bullet_count >= self.dan_trong_chuoi:
                    if self.skill == 1: self.last_skill_shot1 = now
                    elif self.skill == 2: self.last_skill_shot2 = now
                    
                    self.skill = 0 # Trả Boss về trạng thái bắn thường
                    self.bullet_count = 0
class Boss2_time:
    def __init__(self, boss):
        self.boss = boss # Nhận vào con Boss để lấy tọa độ và Group đạn
        self.basic_delay = 700
        self.skill_delay1 = 7000
        self.skill_delay2=13000
        self.dan_trong_chuoi= 13
        self.last_basic_shot = pygame.time.get_ticks()
        self.last_skill_shot1 = pygame.time.get_ticks()
        self.last_skill_shot2=pygame.time.get_ticks()
        self.skill=0
        self.bullet_count = 0
        self.last_bullet_time = 0
        self.time_between_bullets = 100 
    def update(self, now,player_x,player_y):
                bullet_class = boss_bullet_list[1]
                if self.skill == 0:
                    if now - self.last_basic_shot > self.basic_delay:
                        new_bullets = bullet_class.basic_attack(self.boss.rect.centerx, self.boss.rect.bottom)
                        self.boss.bullets.add(*new_bullets)
                        self.last_basic_shot = now
                    if now - self.last_skill_shot2 > self.skill_delay2:
                        self.skill = 2
                        self.bullet_count = 0
                    elif now - self.last_skill_shot1 > self.skill_delay1:
                        self.skill = 1
                        self.bullet_count = 0
                else:
                    if now - self.last_bullet_time > self.time_between_bullets:
                        if self.skill == 1:
                            new_bullets = bullet_class.special_attack1(self.boss.rect.centerx, self.boss.rect.bottom)
                        elif self.skill == 2:
                          new_bullets = bullet_class.special_attack2(
                              self.boss.rect.centerx, self.boss.rect.bottom,
                              player_x,       
                              player_y,
                              toc_do=7, 
                              loaidan='dai')
                        self.boss.bullets.add(*new_bullets)
                        self.bullet_count += 1
                        self.last_bullet_time = now
                        if self.bullet_count >= self.dan_trong_chuoi:
                            if self.skill == 1: self.last_skill_shot1 = now
                            elif self.skill == 2: self.last_skill_shot2 = now
                            
                            self.skill = 0 # Trả Boss về trạng thái bắn thường
                            self.bullet_count = 0
class Boss3_time:
    def __init__(self, boss):
        self.boss = boss # Nhận vào con Boss để lấy tọa độ và Group đạn
        self.basic_delay = 800
        self.skill_delay1 = 8000
        self.skill_delay2=12000
        self.dan_trong_chuoi= 10
        self.last_basic_shot = pygame.time.get_ticks()
        self.last_skill_shot1 = pygame.time.get_ticks()
        self.last_skill_shot2=pygame.time.get_ticks()
        self.skill=0
        self.bullet_count = 0
        self.last_bullet_time = 0
        self.time_between_bullets = 100
    def update(self, now,player_x,player_y):
        bullet_class = boss_bullet_list[2]
        if self.skill == 0:
            if now - self.last_basic_shot > self.basic_delay:
                new_bullets = bullet_class.basic_attack(self.boss.rect.centerx, self.boss.rect.bottom)
                self.boss.bullets.add(*new_bullets)
                self.last_basic_shot = now
            if now - self.last_skill_shot2 > self.skill_delay2:
                self.skill = 2
                self.bullet_count = 0
            elif now - self.last_skill_shot1 > self.skill_delay1:
                self.skill = 1
                self.bullet_count = 0
        else:
            if now - self.last_bullet_time > self.time_between_bullets:
                if self.skill == 1:
                    new_bullets = bullet_class.special_attack1(self.boss.rect.centerx, self.boss.rect.bottom)
                elif self.skill == 2:
                    new_bullets=bullet_class.special_attack2(self.boss.rect.centerx, self.boss.rect.bottom, so_luong_moi_canh=6, spacing=20, toc_do=5, loaidan='dai')
                self.boss.bullets.add(*new_bullets)
                self.bullet_count += 1
                self.last_bullet_time = now
                if self.bullet_count >= self.dan_trong_chuoi:
                    if self.skill == 1: self.last_skill_shot1 = now
                    elif self.skill == 2: self.last_skill_shot2 = now
                    
                    self.skill = 0 # Trả Boss về trạng thái bắn thường
                    self.bullet_count = 0
#code boss3 vaf them vao list
boss_time_list=[Boss1_time,Boss2_time,Boss3_time]