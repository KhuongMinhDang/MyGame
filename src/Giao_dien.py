import pygame

class giao_dien:
    def __init__(self, screen):
        self.screen = screen
        # Load anh nen
        self.nen = pygame.image.load('asset/image/ui/haha.png').convert_alpha()
        #self.nen = pygame.transform.scale(self.nen, (800,800))
        self.nen = pygame.transform.smoothscale(self.nen, (800, 750))

        # Load anh cac nut
        self.game = pygame.image.load('asset/image/ui/game-3.png').convert_alpha()
        self.game = pygame.transform.scale(self.game, (150, 60))

        self.setting = pygame.image.load('asset/image/ui/setting-3.png').convert_alpha()
        self.setting = pygame.transform.scale(self.setting, (150, 60))

        self.stop = pygame.image.load('asset/image/ui/stop-3.png').convert_alpha()
        self.stop = pygame.transform.scale(self.stop, (150, 60))

        self.leaderboard_btn = pygame.image.load('asset/image/ui/leaderboard.png').convert_alpha()
        self.leaderboard_btn = pygame.transform.scale(self.leaderboard_btn, (150, 60))

        # Luu anh va vi tri cac nut
        self.buttons = [
            [self.game, self.game.get_rect(center=(400, 550)), "PLAY"],
            [self.leaderboard_btn, self.leaderboard_btn.get_rect(center=(400, 610)), "LEADERBOARD"],
            [self.setting, self.setting.get_rect(center=(320, 670)), "SETTING"],
            [self.stop, self.stop.get_rect(center=(480, 670)), "EXIT"]
        ]

    def run(self):
        self.screen.blit(self.nen, (0, 0))

        pos = pygame.mouse.get_pos()
        self.selected = -1

        # Xac dinh nut dang duoc tro chuot
        for i, (image, rect, text) in enumerate(self.buttons):
            if rect.collidepoint(pos):
                self.selected = i
                break

        # Ve cac nut va tam giac
        for i, (image, rect, text) in enumerate(self.buttons):
            self.screen.blit(image, rect)

            if i == self.selected:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 255),
                    [
                        (rect.left - 20, rect.centery - 8),
                        (rect.left - 20, rect.centery + 8),
                        (rect.left - 5, rect.centery)
                    ]
                )
class Setting:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((500, 400), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.screen.get_rect().center)
        self.title_font = pygame.font.Font("asset/image/ui/font.ttf", 36)
        self.font = pygame.font.Font("asset/image/ui/font.ttf", 20)
        self.small_font = pygame.font.Font("asset/image/ui/font.ttf", 20)
        self.volume = pygame.mixer.music.get_volume()
        self.muted = False
        self.dragging_slider = False

        self.slider_rect = pygame.Rect(90, 205, 320, 8)
        self.toggle_rect = pygame.Rect(150, 260, 200, 50)
        self.back_rect = pygame.Rect(150, 330, 200, 45)

    def _set_volume_from_position(self, mouse_x):
        local_x = mouse_x - self.rect.left
        self.volume = max(
            0.0,
            min(1.0, (local_x - self.slider_rect.left) / self.slider_rect.width),
        )
        pygame.mixer.music.set_volume(0.0 if self.muted else self.volume)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_slider = False
            return False

        if event.type == pygame.MOUSEMOTION and self.dragging_slider:
            self._set_volume_from_position(event.pos[0])
            return False

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        local_pos = (
            event.pos[0] - self.rect.left,
            event.pos[1] - self.rect.top,
        )
        if self.slider_rect.inflate(20, 24).collidepoint(local_pos):
            self.dragging_slider = True
            self._set_volume_from_position(event.pos[0])
        elif self.toggle_rect.collidepoint(local_pos):
            self.muted = not self.muted
            pygame.mixer.music.set_volume(0.0 if self.muted else self.volume)
        elif self.back_rect.collidepoint(local_pos):
            return True
        return False

    def run(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        self.surface.fill((18, 24, 55, 245))
        pygame.draw.rect(
            self.surface,
            (100, 190, 255),
            self.surface.get_rect(),
            3,
            border_radius=18,
        )

        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        self.surface.blit(title, title.get_rect(center=(250, 85)))

        volume_label = self.font.render("MUSIC VOLUME", True, (220, 230, 255))
        self.surface.blit(volume_label, volume_label.get_rect(center=(250, 155)))

        pygame.draw.rect(self.surface, (70, 80, 110), self.slider_rect, border_radius=4)
        filled_width = int(self.slider_rect.width * self.volume)
        if filled_width:
            pygame.draw.rect(
                self.surface,
                (70, 190, 255),
                (self.slider_rect.left, self.slider_rect.top, filled_width, self.slider_rect.height),
                border_radius=4,
            )
        knob_x = self.slider_rect.left + filled_width
        pygame.draw.circle(
            self.surface,
            (255, 255, 255),
            (knob_x, self.slider_rect.centery),
            12,
        )
        percent = self.small_font.render(f"{int(self.volume * 100)}%", True, (255, 255, 255))
        self.surface.blit(percent, percent.get_rect(center=(250, 230)))

        toggle_color = (130, 55, 65) if self.muted else (40, 125, 90)
        pygame.draw.rect(self.surface, toggle_color, self.toggle_rect, border_radius=10)
        toggle_label = self.font.render(
            "MUSIC: OFF" if self.muted else "MUSIC: ON",
            True,
            (255, 255, 255),
        )
        self.surface.blit(
            toggle_label,
            toggle_label.get_rect(center=self.toggle_rect.center),
        )

        pygame.draw.rect(self.surface, (65, 75, 110), self.back_rect, border_radius=10)
        back_label = self.font.render("BACK", True, (255, 255, 255))
        self.surface.blit(
            back_label,
            back_label.get_rect(center=self.back_rect.center),
        )

        self.screen.blit(self.surface, self.rect)