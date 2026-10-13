import pygame
from src.BossBullet import boss_bullet_list

class Boss1_time:
    def __init__(self, boss):
        self.boss = boss # Nhận vào con Boss để lấy tọa độ và Group đạn
        self.basic_delay = 800
        self.skill_delay = 8000
        self.dan_trong_chuoi= 10
        self.last_basic_shot = pygame.time.get_ticks()
        self.last_skill_shot = pygame.time.get_ticks()
        self.is_using_skill = False
        self.bullet_count = 0
        self.last_bullet_time = 0
        self.time_between_bullets = 100
        self.current_delay = self.time_between_bullets

    def update(self, now):
        bullet_class = boss_bullet_list[0]
        if not self.is_using_skill:
            if now - self.last_basic_shot > self.basic_delay:
                # Bắn đạn thường
                new_bullets = bullet_class.basic_attack(self.boss.rect.centerx, self.boss.rect.bottom)
                self.boss.bullets.add(*new_bullets)
                self.last_basic_shot = now
                
            if now - self.last_skill_shot > self.skill_delay:
                self.is_using_skill = True
                self.bullet_count = 0
                self.last_bullet_time = now
        else:
            if now - self.last_bullet_time > self.current_delay:
                # Bắn đạn đặc biệt
                new_bullets = bullet_class.special_attack(self.boss.rect.centerx, self.boss.rect.bottom)
                self.boss.bullets.add(*new_bullets)
                self.bullet_count += 1
                self.last_bullet_time = now
                self.current_delay = self.time_between_bullets
                
                if self.bullet_count >= self.dan_trong_chuoi:
                    self.bullet_count = 0
                    self.is_using_skill = False
                    self.last_skill_shot = now
#code boss2 vaf them vao list
boss_time_list=[Boss1_time]