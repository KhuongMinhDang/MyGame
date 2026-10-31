import pygame
from src.RecordManager import RecordManager


class Leaderboard:
    """Màn hình Bảng Kỷ Lục hiển thị thời gian tiêu diệt Boss theo từng loại Boss và Phi thuyền."""

    def __init__(self, screen, record_manager: RecordManager):
        self.screen = screen
        self.record_manager = record_manager

        # Font chữ
        try:
            self.title_font = pygame.font.Font("asset/image/ui/font.ttf", 36)
            self.num_font = pygame.font.Font("asset/image/ui/font.ttf", 22)
        except Exception:
            self.title_font = pygame.font.SysFont("arial", 36, bold=True)
            self.num_font = pygame.font.SysFont("arial", 22, bold=True)
        self.label_font = pygame.font.SysFont("arial", 18, bold=True)
        self.sub_font = pygame.font.SysFont("arial", 14)

        # Background
        try:
            self.bg_image = pygame.image.load("asset/image/ui/background.jpg").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (800, 750))
        except Exception:
            self.bg_image = None

        # Nút Back
        try:
            self.back = pygame.image.load("asset/image/ui/back-3.png").convert_alpha()
            self.back = pygame.transform.scale(self.back, (140, 60))
        except Exception:
            self.back = pygame.Surface((120, 50))
            self.back.fill((180, 40, 40))
        self.back_rect = self.back.get_rect(center=(720, 40))

        # Danh sách Boss tab (0, 1, 2)
        self.selected_boss = 0
        self.boss_tabs = []
        boss_names = ["BOSS 1", "BOSS 2", "BOSS 3"]
        tab_w, tab_h = 180, 115
        for i in range(1, 4):
            try:
                img = pygame.image.load(f"asset/image/SpaceShips/boss{i}.png").convert_alpha()
                thumb = pygame.transform.scale(img, (100, 70))
            except Exception:
                thumb = pygame.Surface((100, 70))
                thumb.fill((100, 100, 100))
            rect = pygame.Rect(0, 0, tab_w, tab_h)
            rect.center = (200 + (i - 1) * 200, 138)
            self.boss_tabs.append({
                "id": i - 1,
                "name": boss_names[i - 1],
                "image": thumb,
                "rect": rect
            })

        # Danh sách Phi thuyền (0, 1, 2, 3)
        self.ship_info = []
        ship_weapons = [
            ("SHIP 1", "CYAN BULLET", (0, 240, 255)),
            ("SHIP 2", "RED LASER", (255, 60, 60)),
            ("SHIP 3", "TRIPLE BOUNCE", (255, 180, 0)),
            ("SHIP 4", "DUAL PARALLEL", (0, 230, 255)),
        ]
        for i in range(1, 5):
            try:
                img = pygame.image.load(f"asset/image/SpaceShips/Ship_{i}.png").convert_alpha()
                w, h = img.get_size()
                scale = 65 / max(w, h)
                thumb = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
            except Exception:
                thumb = pygame.Surface((60, 60))
                thumb.fill((80, 80, 80))
            self.ship_info.append({
                "id": i - 1,
                "name": ship_weapons[i - 1][0],
                "weapon": ship_weapons[i - 1][1],
                "color": ship_weapons[i - 1][2],
                "image": thumb
            })

    def handle_event(self, event) -> str | None:
        """Xử lý click chuột và phím. Trả về 'BACK' nếu muốn quay lại."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_rect.collidepoint(event.pos):
                return "BACK"
            for tab in self.boss_tabs:
                if tab["rect"].collidepoint(event.pos):
                    self.selected_boss = tab["id"]
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "BACK"
            elif event.key == pygame.K_LEFT:
                self.selected_boss = (self.selected_boss - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.selected_boss = (self.selected_boss + 1) % 3
            elif event.key in (pygame.K_1, pygame.K_KP1):
                self.selected_boss = 0
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.selected_boss = 1
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.selected_boss = 2

        return None

    def draw(self):
        # 1. Vẽ hình nền
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((15, 15, 25))

        # Phủ lớp tối mờ để text nổi bật
        overlay = pygame.Surface((800, 750), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 200))
        self.screen.blit(overlay, (0, 0))

        # 2. Tiêu đề
        title = self.title_font.render("LEADERBOARD", True, (255, 220, 0))
        title_rect = title.get_rect(center=(400, 45))
        # Hiệu ứng bóng đổ
        shadow = self.title_font.render("LEADERBOARD", True, (80, 50, 0))
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)

        # Nút Back
        self.screen.blit(self.back, self.back_rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.back_rect.collidepoint(mouse_pos):
            pygame.draw.polygon(
                self.screen,
                (255, 255, 255),
                [
                    (self.back_rect.left - 15, self.back_rect.centery - 8),
                    (self.back_rect.left - 15, self.back_rect.centery + 8),
                    (self.back_rect.left - 3, self.back_rect.centery),
                ],
            )

        # 3. Vẽ các tab Boss (khung mở rộng ôm trọn ảnh và tên Boss)
        for tab in self.boss_tabs:
            is_active = tab["id"] == self.selected_boss
            rect = tab["rect"]

            # Nền tab
            tab_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            if is_active:
                tab_surf.fill((40, 60, 110, 220))
                pygame.draw.rect(tab_surf, (255, 220, 0), (0, 0, rect.width, rect.height), 3, border_radius=12)
            else:
                tab_surf.fill((20, 25, 45, 170))
                pygame.draw.rect(tab_surf, (80, 100, 140), (0, 0, rect.width, rect.height), 1, border_radius=12)

            self.screen.blit(tab_surf, rect.topleft)

            # Ảnh Boss
            img_rect = tab["image"].get_rect(center=(rect.centerx, rect.top + 42))
            self.screen.blit(tab["image"], img_rect)

            # Tên Boss nhỏ ở dưới tab (nằm trọn bên trong khung với khoảng đệm đẹp mắt)
            name_color = (255, 230, 100) if is_active else (180, 190, 210)
            name_txt = self.sub_font.render(tab["name"], True, name_color)
            self.screen.blit(name_txt, name_txt.get_rect(center=(rect.centerx, rect.bottom - 18)))

            # Con trỏ tam giác nếu tab đang chọn (nằm dưới đáy khung)
            if is_active:
                pygame.draw.polygon(
                    self.screen,
                    (255, 220, 0),
                    [
                        (rect.centerx - 9, rect.bottom + 4),
                        (rect.centerx + 9, rect.bottom + 4),
                        (rect.centerx, rect.bottom + 14)
                    ]
                )

        # 4. Tìm thời gian tốt nhất của Boss này để gắn cờ vàng
        records_for_boss = []
        for ship in self.ship_info:
            rec = self.record_manager.get_record(self.selected_boss, ship["id"])
            if rec is not None:
                records_for_boss.append(rec)
        fastest_record = min(records_for_boss) if records_for_boss else None

        # 5. Khung danh sách kỷ lục 4 máy bay
        list_y_start = 225
        card_h = 110
        gap = 15

        for i, ship in enumerate(self.ship_info):
            card_y = list_y_start + i * (card_h + gap)
            record_val = self.record_manager.get_record(self.selected_boss, ship["id"])
            is_fastest = (record_val is not None and record_val == fastest_record)

            # Thẻ bo góc bán trong suốt
            card = pygame.Surface((700, card_h), pygame.SRCALPHA)
            if is_fastest:
                card.fill((45, 40, 20, 220))
                border_color = (255, 215, 0)
                border_w = 2
            else:
                card.fill((25, 30, 50, 200))
                border_color = (60, 80, 120)
                border_w = 1

            pygame.draw.rect(card, border_color, (0, 0, 700, card_h), border_w, border_radius=12)
            self.screen.blit(card, (50, card_y))

            # Ảnh phi thuyền (bên trái)
            img_center = (115, card_y + card_h // 2)
            self.screen.blit(ship["image"], ship["image"].get_rect(center=img_center))

            # Thông tin tàu: Tên và Vũ khí
            name_surf = self.label_font.render(ship["name"], True, (255, 255, 255))
            self.screen.blit(name_surf, (185, card_y + 24))

            wep_surf = self.sub_font.render(f"Weapon: {ship['weapon']}", True, ship["color"])
            self.screen.blit(wep_surf, (185, card_y + 58))

            # Huy hiệu BEST OF BOSS nếu đây là tàu nhanh nhất
            if is_fastest:
                badge = self.sub_font.render("[ TOP SPEED ]", True, (255, 220, 50))
                self.screen.blit(badge, (360, card_y + 26))

            # Thời gian kỷ lục (bên phải)
            time_str = self.record_manager.format_time(record_val)
            if record_val is not None:
                if is_fastest:
                    time_color = (255, 220, 0)
                else:
                    time_color = (100, 240, 255)
            else:
                time_color = (140, 140, 140)

            time_label = self.sub_font.render("BEST RECORD", True, (170, 180, 200))
            self.screen.blit(time_label, (550, card_y + 24))

            time_surf = self.num_font.render(time_str, True, time_color)
            self.screen.blit(time_surf, (550, card_y + 50))

        # 6. Hướng dẫn phím ở đáy màn hình
        tip = self.sub_font.render("Use LEFT/RIGHT arrows or 1-3 keys to switch Boss | ESC to return", True, (150, 160, 180))
        self.screen.blit(tip, tip.get_rect(center=(400, 730)))

