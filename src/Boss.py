import pygame
import random
from src.BossBullet import boss_bullet_list
from src.Boss_time import boss_time_list
from src.Player import player
from src.Sound import sound
from src.Exp import Explosion
class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_id=1):
        super().__init__()
        self.boss_id = boss_id
        #them anh boss vo day
        self.image_boss = [
            pygame.transform.scale(pygame.image.load('asset/image/SpaceShips/boss1.png').convert_alpha(),(289,216)),
            pygame.transform.scale(pygame.image.load('asset/image/SpaceShips/boss2.png').convert_alpha(),(300,209)),
            pygame.transform.scale(pygame.image.load('asset/image/SpaceShips/boss3.png').convert_alpha(),(289,216))
        ]
        self.image = self.image_boss[self.boss_id]
        self.rect = self.image.get_rect(midtop=(400, -200))
        #am thanh
        self.sound=sound()
        # Hitbox nhỏ ở thân boss (chỉnh số cho vừa ý)
        HITBOX_W, HITBOX_H = 150, 140
        self.hitbox = pygame.Rect(0, 0, HITBOX_W, HITBOX_H)
        self.hitbox.center = self.rect.center

        if self.boss_id==0: self.hp=1500
        else: self.hp=2000
        self.max_hp = self.hp
        self.bullets = pygame.sprite.Group() # Nhóm chứa đạn của boss này
        self.dang_bay = True
        self.speed_x = 0
        self.speed_y = 4
        self.move_timer = pygame.time.get_ticks() 
        self.co_che=boss_time_list[self.boss_id](self)
        #boss dang no
        self.explosions_group = pygame.sprite.Group()
        self.is_dying = False
        self.death_timer = 0
        self.last_explosion_time = 0
    def luong_mau(self, damage):
        if not self.is_dying: # Chặn không cho trừ máu tiếp khi đang hấp hối
            self.hp -= damage
            if self.hp <= 0:
                self.is_dying = True
                self.death_timer = pygame.time.get_ticks()
                self.sound.play_explosion()
    def update(self,player):
        now = pygame.time.get_ticks()
        if self.is_dying:
            # Cứ 100ms tạo ngẫu nhiên 1 vụ nổ trên thân Boss
            if now - self.last_explosion_time > 100:
                ex = random.randint(self.rect.left, self.rect.right)
                ey = random.randint(self.rect.top, self.rect.bottom)
                self.explosions_group.add(Explosion(ex, ey))
                self.last_explosion_time = now
                
            self.explosions_group.update()
            
            # Trì hoãn cái chết 1.5 giây (1500ms) rồi mới xóa Boss hoàn toàn
            if now - self.death_timer > 2000:
                self.kill()
                
            return
        #dang nhoai manf hinh
        if self.dang_bay:
            self.rect.y += self.speed_y
            if self.rect.y >= 20:
                self.rect.y = 20
                self.dang_bay = False 
                self.speed_x = random.choice([-3, 3])        
        #luc vao man hinh
        else:
            toc_do_di_chuyen = self.speed_x
            
            # 2. CHỈNH SỬA TỐC ĐỘ GỌN GÀNG TẠI ĐÂY
            # Nếu Boss đang tung chiêu (bất kỳ skill nào khác 0)
            if self.co_che.skill != 0:
                
                # TRƯỜNG HỢP NGOẠI LỆ: Boss 2 dùng Skill 1 thì đứng im
                if self.boss_id == 1 and self.co_che.skill == 1:
                    toc_do_di_chuyen = 0
                
                # CÁC TRƯỜNG HỢP CÒN LẠI: Dịch nhẹ 1 pixel như cũ
                else:
                    if self.speed_x > 0:
                        toc_do_di_chuyen = 1
                    elif self.speed_x < 0:
                        toc_do_di_chuyen = -1

            # 3. Áp dụng di chuyển vào tọa độ
            self.rect.x += toc_do_di_chuyen

            # 4. CHẶN VIỀN MÀN HÌNH (Giữ nguyên)
            if self.rect.left <= 0:
                self.rect.left = 0
                self.speed_x = random.randint(2, 4) 
            elif self.rect.right >= 800: 
                self.rect.right = 800
                self.speed_x = random.randint(-4, -2) 
                
            # 5. ĐỔI HƯỚNG TỰ ĐỘNG (Giữ nguyên)
            if now - self.move_timer > 2000: 
                self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])
                self.move_timer = now
            self.co_che.update(now,player.rect.centerx,player.rect.centery)#luc ban dan

        # Cập nhật hitbox theo rect (nằm ngoài if/else)
        self.hitbox.center = self.rect.center
