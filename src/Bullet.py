import pygame
import math


# 1. LỚP ĐẠN THƯỜNG 
class Bullet(pygame.sprite.Sprite):
    kind = "BULLET"

    def __init__(self, player, color='white', speed=10, size=(10, 18)):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=player.rect.midtop)

    def update(self):
        # Quỹ đạo bay thẳng lên trên
        self.rect.y -= self.speed
        if self.rect.bottom < -10:
            self.kill()


# 2. LỚP TIA LAZE 
class LaserBeam(pygame.sprite.Sprite):
    kind = "LASER"

    def __init__(self, player, base_width=14, color=(0, 240, 255)):
        super().__init__()
        self.player = player
        self.base_width = base_width
        self.color = color
        self.update()

    def update(self):
        # Quỹ đạo luôn dính liền với đỉnh đầu tàu và kéo lên đỉnh màn hình
        beam_height = max(1, self.player.rect.top)

        ticks = pygame.time.get_ticks()
        pulse = math.sin(ticks * 0.02) * 2
        width = int(max(6, self.base_width + pulse))

        self.image = pygame.Surface((width, beam_height), pygame.SRCALPHA)

        # Hào quang phát sáng ngoài
        outer_glow = (*self.color, 80)
        pygame.draw.rect(self.image, outer_glow, (0, 0, width, beam_height))

        # Dải sáng bên trong
        inner_width = max(4, width // 2)
        inner_x = (width - inner_width) // 2
        inner_glow = (*self.color, 190)
        pygame.draw.rect(self.image, inner_glow, (inner_x, 0, inner_width, beam_height))

        # Lõi năng lượng trắng ở giữa
        core_width = max(2, width // 4)
        core_x = (width - core_width) // 2
        pygame.draw.rect(self.image, (255, 255, 255), (core_x, 0, core_width, beam_height))

        # Đốm sáng lóe tại nòng súng
        flare_radius = width // 2 + 3
        pygame.draw.circle(self.image, (255, 255, 255), (width // 2, beam_height - 2), flare_radius)
        pygame.draw.circle(self.image, (*self.color, 140), (width // 2, beam_height - 2), flare_radius + 4)

        self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)

# 3. LỚP ĐẠN NẢY
class BouncingBullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed_x, speed_y, color=(255, 140, 0), size=(12, 20)):
        super().__init__()
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

        # Tạo hình ảnh đạn hình elip phát sáng neon với lõi trắng
        self.base_image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(self.base_image, (*color, 120), (0, 0, size[0], size[1]))
        pygame.draw.ellipse(self.base_image, color, (1, 2, size[0] - 2, size[1] - 4))
        pygame.draw.ellipse(self.base_image, (255, 255, 255), (3, 4, size[0] - 6, size[1] - 8))

        self.rect = self.base_image.get_rect(center=pos)
        self.update_image()

    def update_image(self):
        # Xoay hình ảnh đạn hướng theo vector vận tốc
        angle = -math.degrees(math.atan2(self.speed_x, -self.speed_y))
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Nảy khi chạm mép trái (0) hoặc mép phải (800)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)
            self.update_image()
        elif self.rect.right >= 800:
            self.rect.right = 800
            self.speed_x = -abs(self.speed_x)
            self.update_image()

        # Tự hủy khi bay ra khỏi mép trên màn hình
        if self.rect.bottom < -10:
            self.kill()

class ParallelBullet(pygame.sprite.Sprite):
    """Từng viên đạn đơn trong cặp đạn song song"""
    def __init__(self, pos, speed=11, color=(0, 230, 255), size=(10, 20)):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # Hào quang phát sáng neon ngoài
        pygame.draw.ellipse(self.image, (*color, 120), (0, 0, size[0], size[1]))
        # Thân đạn màu chính
        pygame.draw.ellipse(self.image, color, (1, 2, size[0] - 2, size[1] - 4))
        # Lõi trắng sáng ở giữa
        pygame.draw.ellipse(self.image, (255, 255, 255), (3, 4, size[0] - 6, size[1] - 8))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < -10:
            self.kill()

# --- 4. ĐỊNH NGHĨA CÁC LOẠI ĐẠN CỤ THỂ ---
class NormalBullet(Bullet):
    damage=10
    """Đạn thường màu xanh cyan bay thẳng"""
    def __init__(self, player):
        super().__init__(player, color=(0, 255, 255), speed=10)


class RedLaser(LaserBeam):
    damage=10
    """Tia Laze Đỏ rực chiếu liên tục"""
    def __init__(self, player):
        super().__init__(player, base_width=14, color=(255, 60, 60))



class BounceTripleBullet:
    """Loại đạn bắn 3 viên: 1 viên thẳng và 2 viên chéo nảy ở 2 rìa màn hình"""
    kind = "BULLET"
    damage=1.5
    def __new__(cls, player):
        pos = player.rect.midtop
        # 1 viên thẳng ở giữa
        b_mid = BouncingBullet(pos, speed_x=0, speed_y=-11, color=(255, 220, 0))
        # 1 viên chéo sang trái (nảy khi chạm rìa trái)
        b_left = BouncingBullet(pos, speed_x=-9.5, speed_y=-4.5, color=(255, 130, 0))
        # 1 viên chéo sang phải (nảy khi chạm rìa phải)
        b_right = BouncingBullet(pos, speed_x=9.5, speed_y=-4.5, color=(255, 130, 0))
        b_mid.damage = 1.5
        b_left.damage = 1.5
        b_right.damage = 1.5
        return [b_mid, b_left, b_right]



class DualParallelBullet:
    damage=5
    """Loại đạn bắn 2 viên bay song song từ 2 bên cánh phi thuyền"""
    kind = "BULLET"

    def __new__(cls, player, offset_x=22, speed=11, color=(0, 230, 255)):
        center_x = player.rect.centerx
        top_y = player.rect.top
        # Viên cánh trái
        b_left = ParallelBullet((center_x - offset_x, top_y + 10), speed=speed, color=color)
        # Viên cánh phải
        b_right = ParallelBullet((center_x + offset_x, top_y + 10), speed=speed, color=color)
        b_left.damage = 5
        b_right.damage = 5

        return [b_left, b_right]


# --- 5. DANH SÁCH CÁC LOẠI ĐẠN ĐI CÙNG TỪNG PLAYER ---
# player[0] -> bullet_list[0] (Đạn thường trắng)
# player[1] -> bullet_list[1] (Laze Đỏ)
# player[2] -> bullet_list[2] (Đạn 3 tia: thẳng + 2 tia chéo nảy tường)
# player[3] -> bullet_list[3] (Đạn đôi bay song song)
bullet_list = [
    NormalBullet,
    RedLaser,
    BounceTripleBullet,
    DualParallelBullet
]


