import pygame
from src.BossBullet import boss_bullet_list
class BossTimeBase:
    """Class gốc quản lý vòng lặp xả đạn chung cho mọi Boss"""
    def __init__(self, boss, bullet_idx, basic_delay=800, skill_delay1=8000, skill_delay2=12000, dan_trong_chuoi=10):
        self.boss = boss
        self.bullet_class = boss_bullet_list[bullet_idx]
        self.basic_delay = basic_delay
        self.skill_delay1 = skill_delay1
        self.skill_delay2 = skill_delay2
        self.dan_trong_chuoi = dan_trong_chuoi
        t = pygame.time.get_ticks()
        self.last_basic_shot, self.last_skill_shot1, self.last_skill_shot2 = t, t, t
        self.skill, self.bullet_count = 0, 0
        self.last_bullet_time = 0
        self.time_between_bullets = 100
    def update(self, now, player_x, player_y):
        if self.skill == 0:
            if now - self.last_basic_shot > self.basic_delay:
                self.boss.bullets.add(*self.bullet_class.basic_attack(self.boss.rect.centerx, self.boss.rect.bottom))
                self.last_basic_shot = now
            if now - self.last_skill_shot2 > self.skill_delay2:
                self.skill, self.bullet_count = 2, 0
            elif now - self.last_skill_shot1 > self.skill_delay1:
                self.skill, self.bullet_count = 1, 0
        else:
            if now - self.last_bullet_time > self.time_between_bullets:
                new_bullets = self.fire_skill(player_x, player_y)
                if new_bullets:
                    self.boss.bullets.add(*new_bullets) 
                self.bullet_count += 1
                self.last_bullet_time = now
                if self.bullet_count >= self.dan_trong_chuoi:
                    if self.skill == 1: self.last_skill_shot1 = now
                    elif self.skill == 2: self.last_skill_shot2 = now
                    self.skill, self.bullet_count = 0, 0
    def fire_skill(self, px, py):
        return []
class Boss1_time(BossTimeBase):
    def __init__(self, boss):
        super().__init__(boss, bullet_idx=0, dan_trong_chuoi=10)
    def fire_skill(self, px, py):
        bx, by = self.boss.rect.centerx, self.boss.rect.bottom
        if self.skill == 1: return self.bullet_class.special_attack1(bx, by)
        if self.skill == 2: return self.bullet_class.special_attack2(bx, by)

class Boss2_time(BossTimeBase):
    def __init__(self, boss):
        super().__init__(boss, bullet_idx=1, basic_delay=700, skill_delay1=7000, skill_delay2=13000, dan_trong_chuoi=13)
    def fire_skill(self, px, py):
        bx, by = self.boss.rect.centerx, self.boss.rect.bottom
        if self.skill == 1: return self.bullet_class.special_attack1(bx, by)
        if self.skill == 2: return self.bullet_class.special_attack2(bx, by, px, py, toc_do=7, loaidan='dai')

class Boss3_time(BossTimeBase):
    def __init__(self, boss):
        super().__init__(boss, bullet_idx=2, dan_trong_chuoi=10)
    def fire_skill(self, px, py):
        bx, by = self.boss.rect.centerx, self.boss.rect.bottom
        if self.skill == 1: return self.bullet_class.special_attack1(bx, by)
        if self.skill == 2: return self.bullet_class.special_attack2(bx, by, so_luong_moi_canh=6, spacing=20, toc_do=5, loaidan='dai')

boss_time_list = [Boss1_time, Boss2_time, Boss3_time]