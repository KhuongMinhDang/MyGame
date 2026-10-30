import pygame
class player(pygame.sprite.Sprite):
    def __init__(self, x=0):
        super().__init__()
        self.ship_id = x
        #hp
        self.hp=pygame.image.load("asset/image/ui/hp-0.png").convert_alpha()
        self.hp=pygame.transform.scale(self.hp, (70, 70))
        # 1. Quản lý hình ảnh phi thuyền
        self.image_ship = [
            pygame.image.load('asset/image/SpaceShips/Ship_1.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_2.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_3.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_4.png').convert_alpha()
        ]
        self.image = self.image_ship[x]
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * 1.5), int(h * 1.5)))
        self.rect = self.image.get_rect(center=(400, 600))
        # Hitbox nhỏ ở giữa thân tàu (chỉnh 2 số này cho vừa ý)
        HITBOX_W, HITBOX_H = 20, 20
        self.hitbox = pygame.Rect(0, 0, HITBOX_W, HITBOX_H)
        self.hitbox.center = self.rect.center

        # Thời gian tác dụng của vật phẩm (tính theo mili-giây)
        self.invincible_until = 0
        self.double_damage_until = 0

    def activate_invincible(self, now, duration=10000):
        self.invincible_until = now + duration

    def activate_double_damage(self, now, duration=10000):
        self.double_damage_until = now + duration

    def is_invincible(self, now):
        return now < self.invincible_until

    def is_double_damage(self, now):
        return now < self.double_damage_until

    def update(self, screen):
        import math
        now = pygame.time.get_ticks()

        # 2. Quản lý chuyển động phi thuyền (WASD và Phím Mũi tên)
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.left <= 0: self.rect.left = 0
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.right >= 800: self.rect.right = 800
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= 3
            if self.rect.top <= 0: self.rect.top = 0
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += 3
            if self.rect.bottom >= 750: self.rect.bottom = 750
        self.hitbox.center = self.rect.center

        # 3. Vẽ hiệu ứng hào quang bảo vệ khi BẤT TỬ
        if self.is_invincible(now):
            radius = max(self.rect.width, self.rect.height) // 2 + 10
            pulse = int(math.sin(now * 0.015) * 3)
            shield_surf = pygame.Surface(((radius + 10) * 2, (radius + 10) * 2), pygame.SRCALPHA)
            center = (radius + 10, radius + 10)
            pygame.draw.circle(shield_surf, (0, 200, 255, 80), center, radius + pulse)
            pygame.draw.circle(shield_surf, (0, 240, 255, 200), center, radius + pulse, 3)
            pygame.draw.circle(shield_surf, (255, 255, 255, 220), center, radius + pulse - 2, 1)
            screen.blit(shield_surf, shield_surf.get_rect(center=self.rect.center))

        # 4. Vẽ hiệu ứng hào quang rực lửa khi X2 SÁT THƯƠNG
        if self.is_double_damage(now):
            radius = max(self.rect.width, self.rect.height) // 2 + 5
            pulse = int(math.sin(now * 0.02) * 2)
            dmg_surf = pygame.Surface(((radius + 10) * 2, (radius + 10) * 2), pygame.SRCALPHA)
            center = (radius + 10, radius + 10)
            pygame.draw.circle(dmg_surf, (255, 80, 0, 70), center, radius + pulse)
            pygame.draw.circle(dmg_surf, (255, 140, 0, 190), center, radius + pulse, 2)
            screen.blit(dmg_surf, dmg_surf.get_rect(center=self.rect.center))

        # 5. Vẽ thanh HP góc dưới màn hình
        screen.blit(self.hp, (0, 650))
