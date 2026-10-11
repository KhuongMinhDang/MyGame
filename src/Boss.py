import pygame
import random
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > 800:
            self.kill()
class Boss_cha(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image=pygame.transform.scale(self.image,(200,200))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.hp = hp
        self.max_hp = hp
        self.bullets = pygame.sprite.Group() # Nhóm chứa tất cả đạn 
        
        self.last_basic_shot = pygame.time.get_ticks()
        self.basic_delay = 500 # Bắn đạn cơ bản
        
        self.last_skill_shot = pygame.time.get_ticks()
        self.skill_delay = 8000 # Tung chiêu đặc biệt
    def luong_mau(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
    def update(self):
        pass
class Boss1(Boss_cha):
    def __init__(self):
        super().__init__(400,-200, 1000, 'asset/image/SpaceShips/boss1.png')
        self.dang_bay=True
        self.speed_x=0
        self.speed_y=4
        self.move_timer=pygame.time.get_ticks() 
        self.is_using_skill = False      # Công tắc bật/tắt trạng thái xả chiêu
        self.burst_count = 0             # Đếm số chuỗi đã bắn (mục tiêu: 3 chuỗi)
        self.bullet_count = 0            # Đếm số đạn trong 1 chuỗi (mục tiêu: 10 viên)
        
        self.last_bullet_time = 0        # Thời điểm bắn viên đạn gần nhất trong chuỗi
        self.time_between_bullets = 100  # Thời gian giữa 2 viên đạn liên tiếp (100 mili-giây)
        self.current_delay = self.time_between_bullets # Biến điều chỉnh độ trễ hiện tại

    def update(self):
        now = pygame.time.get_ticks()
        
        # Giai đoạn 1: Đi từ ngoài vào 
        if self.dang_bay:
            self.rect.y += self.speed_y
            if self.rect.y >= 20:
                self.rect.y = 20
                self.dang_bay = False 
                self.speed_x = random.choice([-3, 3]) 
                
        # Giai đoạn 2: Chiến đấu
        else:
            # 1. Logic di chuyển
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
                
            # 2. Logic Tấn Công
            if not self.is_using_skill:
                if now - self.last_basic_shot > self.basic_delay:
                    self.basic_attack()
                    self.last_basic_shot = now
                    
                if now - self.last_skill_shot > self.skill_delay:
                    self.is_using_skill = True
                    self.burst_count = 0        # Reset số chuỗi về 0
                    self.bullet_count = 0       # Reset đạn về 0
                    self.last_bullet_time = now # Bắt đầu tính giờ xả đạn
            else:
                # Nếu ĐANG xả chiêu đặc biệt
                if now - self.last_bullet_time > self.current_delay:
                    # Bắn 1 viên đạn tỏa ra
                    self.special_skill_bullet()
                    
                    self.bullet_count += 1
                    self.last_bullet_time = now
                    self.current_delay = self.time_between_bullets # Giữ nhịp đạn bắn nhanh
                    
                    # Kiểm tra xem đã bắn đủ 10 viên cho 1 chuỗi chưa
                    if self.bullet_count >= 10:
                        self.bullet_count = 0 # Reset lại số đạn cho chuỗi sau
                        self.is_using_skill=False
                        self.last_skill_shot=now

                        
                   

    # Bắn cơ bản: 1 viên thẳng
    def basic_attack(self):
        bullet = BossBullet(self.rect.centerx, self.rect.bottom, 0, 5)
        self.bullets.add(bullet)

    # Kỹ năng đặc biệt
    def special_skill_bullet(self):
        b_left = BossBullet(self.rect.centerx, self.rect.bottom, -3, 6)  
        b_mid = BossBullet(self.rect.centerx, self.rect.bottom, 0, 6)    
        b_right = BossBullet(self.rect.centerx, self.rect.bottom, 3, 6)  
        self.bullets.add(b_left, b_mid, b_right)
       
