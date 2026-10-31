import pygame
class Pause:
    def __init__(self,screen):
        self.screen = screen
        self.surface = pygame.Surface((300, 250), pygame.SRCALPHA)
        self.surface.fill((20, 20, 40, 220))
        self.resume = pygame.image.load("asset/image/ui/resume-3.png").convert_alpha();
        self.resume = pygame.transform.scale(self.resume, (150, 60))
        self.restart = pygame.image.load("asset/image/ui/restart-3.png").convert_alpha();
        self.restart = pygame.transform.scale(self.restart, (150, 60))
        self.main_menu= pygame.image.load("asset/image/ui/main_menu-3.png").convert_alpha();
        self.main_menu = pygame.transform.scale(self.main_menu, (150, 60))
        self.buttons = [
            [self.resume, self.resume.get_rect(center=(400, 290)), "resume"],
            [self.restart, self.restart.get_rect(center=(400, 370)), "restart"],
            [self.main_menu, self.main_menu.get_rect(center=(400,450)), "main_menu"]
        ]
    def update(self):
        self.screen.blit(self.surface,self.surface.get_rect(center=self.screen.get_rect().center))
        pos = pygame.mouse.get_pos()
        selected = -1

        # Xac dinh nut dang duoc tro chuot
        for i, (image, rect, text) in enumerate(self.buttons):
            if rect.collidepoint(pos):
                selected = i
                break

        # Ve cac nut va tam giac
        for i, (image, rect, text) in enumerate(self.buttons):
            self.screen.blit(image, rect)

            if i == selected:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 255),
                    [
                        (rect.left - 20, rect.centery - 8),
                        (rect.left - 20, rect.centery + 8),
                        (rect.left - 5, rect.centery)
                    ]
                )
class Result:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font("asset/image/ui/font.ttf", 46)
            self.sub_font = pygame.font.Font("asset/image/ui/font.ttf", 22)
            self.badge_font = pygame.font.Font("asset/image/ui/font.ttf", 20)
        except Exception:
            self.font = pygame.font.SysFont("arial", 46, bold=True)
            self.sub_font = pygame.font.SysFont("arial", 22, bold=True)
            self.badge_font = pygame.font.SysFont("arial", 20, bold=True)

        self.label_font = pygame.font.SysFont("arial", 17, bold=True)
        self.result_now = None

        # Thống kê thời gian
        self.clear_time_str = None
        self.best_time_str = None
        self.is_new_record = False

        self.restart = pygame.image.load("asset/image/ui/restart-3.png").convert_alpha()
        self.restart = pygame.transform.scale(self.restart, (150, 60))
        self.main_menu = pygame.image.load("asset/image/ui/main_menu-3.png").convert_alpha()
        self.main_menu = pygame.transform.scale(self.main_menu, (150, 60))
        self.buttons = [
            [self.restart, self.restart.get_rect(center=(300, 420)), "restart"],
            [self.main_menu, self.main_menu.get_rect(center=(500, 420)), "main_menu"]
        ]

    def set_stats(self, clear_time_str: str, best_time_str: str, is_new_record: bool = False):
        """Cập nhật dữ liệu thời gian trận đấu để hiển thị khi chiến thắng."""
        self.clear_time_str = clear_time_str
        self.best_time_str = best_time_str
        self.is_new_record = is_new_record

    def update(self):
        pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()

        if self.result_now == "Win":
            # 1. Bảng nền mờ trung tâm
            panel = pygame.Surface((540, 380), pygame.SRCALPHA)
            panel.fill((12, 18, 32, 225))
            pygame.draw.rect(panel, (255, 215, 0), (0, 0, 540, 380), 2, border_radius=16)
            self.screen.blit(panel, panel.get_rect(center=(400, 310)))

            # 2. Tiêu đề YOU WIN
            title = self.font.render("YOU WIN", True, (255, 215, 0))
            self.screen.blit(title, title.get_rect(center=(400, 155)))

            # 3. Huy hiệu NEW RECORD (nếu phá kỷ lục)
            if self.is_new_record:
                glow_color = (255, 255, 100) if (now // 250) % 2 == 0 else (255, 180, 0)
                badge = self.badge_font.render("★ NEW RECORD! ★", True, glow_color)
                self.screen.blit(badge, badge.get_rect(center=(400, 195)))
                curr_y = 230
            else:
                curr_y = 205

            # 4. Hiển thị thời gian đánh bại
            clear_label = self.label_font.render("DEFEAT TIME:", True, (180, 195, 220))
            self.screen.blit(clear_label, (210, curr_y))

            clear_val = self.clear_time_str or "--:--.--"
            clear_surf = self.sub_font.render(clear_val, True, (0, 240, 255))
            self.screen.blit(clear_surf, (370, curr_y - 2))

            curr_y += 34
            best_label = self.label_font.render("BEST RECORD:", True, (180, 195, 220))
            self.screen.blit(best_label, (210, curr_y))

            best_val = self.best_time_str or "--:--.--"
            best_surf = self.sub_font.render(best_val, True, (255, 220, 80))
            self.screen.blit(best_surf, (370, curr_y - 2))

            # Đường kẻ ngăn cách
            curr_y += 38
            pygame.draw.line(self.screen, (70, 90, 130), (160, curr_y), (640, curr_y), 1)

        else:
            # Giao diện khi THUA (YOU LOSE)
            panel = pygame.Surface((460, 260), pygame.SRCALPHA)
            panel.fill((20, 10, 15, 220))
            pygame.draw.rect(panel, (220, 40, 40), (0, 0, 460, 260), 2, border_radius=14)
            self.screen.blit(panel, panel.get_rect(center=(400, 350)))

            text = self.font.render("YOU LOSE", True, (255, 50, 50))
            self.screen.blit(text, text.get_rect(center=(400, 260)))

        # Xác định nút đang hover
        selected = -1
        for i, (image, rect, text) in enumerate(self.buttons):
            if rect.collidepoint(pos):
                selected = i
                break

        # Vẽ các nút và con trỏ tam giác
        for i, (image, rect, text) in enumerate(self.buttons):
            self.screen.blit(image, rect)
            if i == selected:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 255),
                    [
                        (rect.left - 18, rect.centery - 7),
                        (rect.left - 18, rect.centery + 7),
                        (rect.left - 4, rect.centery)
                    ]
                )
