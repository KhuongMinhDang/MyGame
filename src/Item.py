import pygame
import math
import random


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type  # "DOUBLE_DAMAGE" hoặc "SHIELD"
        self.size = 46
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 14000  # Tồn tại 14 giây nếu không nhặt

        # Tốc độ trôi nhẹ nhàng trong không gian
        self.speed_y = 1.0
        self.t = random.uniform(0, math.pi * 2)

        # Tạo ảnh hiển thị cho vật phẩm
        self.base_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.ve_icon()

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def ve_icon(self):
        center = (self.size // 2, self.size // 2)

        if self.item_type == "DOUBLE_DAMAGE":
            # Icon 2X màu cam/đỏ rực lửa
            pygame.draw.circle(self.base_image, (255, 60, 0, 150), center, self.size // 2)
            pygame.draw.circle(self.base_image, (255, 140, 0), center, self.size // 2 - 2, 3)
            font = pygame.font.SysFont("arial", 20, bold=True)
            txt = font.render("2X", True, (255, 255, 255))
            self.base_image.blit(txt, txt.get_rect(center=center))

        elif self.item_type == "SHIELD":
            # Icon Khiên Bất Tử màu xanh dương / ngọc neon
            pygame.draw.circle(self.base_image, (0, 180, 255, 150), center, self.size // 2)
            pygame.draw.circle(self.base_image, (0, 230, 255), center, self.size // 2 - 2, 3)
            points = [
                (self.size // 2 - 11, self.size // 2 - 10),
                (self.size // 2 + 11, self.size // 2 - 10),
                (self.size // 2 + 11, self.size // 2 + 2),
                (self.size // 2, self.size // 2 + 13),
                (self.size // 2 - 11, self.size // 2 + 2),
            ]
            pygame.draw.polygon(self.base_image, (255, 255, 255), points)
            pygame.draw.polygon(self.base_image, (0, 140, 255), points, 2)

    def update(self):
        now = pygame.time.get_ticks()
        # Tự hủy nếu hết thời gian tồn tại
        if now - self.spawn_time > self.lifetime:
            self.kill()
            return

        # Chuyển động trôi nhẹ nhàng từ từ xuống và đung đưa qua lại
        self.t += 0.04
        self.rect.x += int(math.sin(self.t) * 1.5)
        self.rect.y += self.speed_y

        # Giữ trong màn hình
        if self.rect.left < 20: self.rect.left = 20
        if self.rect.right > 780: self.rect.right = 780
        if self.rect.top > 750:
            self.kill()

        # Nhấp nháy báo hiệu trong 3 giây cuối trước khi biến mất
        time_left = self.lifetime - (now - self.spawn_time)
        if time_left < 3000:
            alpha = 100 if (now // 150) % 2 == 0 else 255
            self.image.set_alpha(alpha)
