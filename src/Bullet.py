import pygame
import math


# --- 1. LỚP ĐẠN THƯỜNG (Quản lý hình ảnh và quỹ đạo bay thẳng) ---
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


# --- 2. LỚP TIA LAZE (Quản lý hình ảnh dải sáng và quỹ đạo bám theo tàu) ---
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


# --- 3. ĐỊNH NGHĨA CÁC LOẠI ĐẠN CỤ THỂ ---
class NormalBullet(Bullet):
    """Đạn thường màu trắng bay thẳng"""
    def __init__(self, player):
        super().__init__(player, color='white', speed=10)


class RedLaser(LaserBeam):
    """Tia Laze Đỏ rực chiếu liên tục"""
    def __init__(self, player):
        super().__init__(player, base_width=14, color=(255, 60, 60))


class YellowBullet(Bullet):
    """Đạn năng lượng màu vàng bay thẳng"""
    def __init__(self, player):
        super().__init__(player, color=(255, 230, 50), speed=12)


class GreenLaser(LaserBeam):
    """Tia Laze Xanh lá chiếu liên tục"""
    def __init__(self, player):
        super().__init__(player, base_width=14, color=(0, 255, 0))


# --- 4. DANH SÁCH CÁC LOẠI ĐẠN ĐI CÙNG TỪNG PLAYER ---
# player[0] -> bullet_list[0] (Đạn thường trắng)
# player[1] -> bullet_list[1] (Laze Đỏ)
# player[2] -> bullet_list[2] (Đạn vàng)
# player[3] -> bullet_list[3] (Laze Xanh)
bullet_list = [
    NormalBullet,
    RedLaser,
    YellowBullet,
    GreenLaser
]
