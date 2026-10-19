import pygame

class giao_dien:
    def __init__(self, screen):
        self.screen = screen
        # Load anh nen
        self.nen = pygame.image.load('asset/image/ui/haha.jpg').convert_alpha()
        #.nen = pygame.transform.scale(self.nen, (800, 800))

        # Load anh cac nut
        self.login = pygame.image.load('asset/image/ui/login.png').convert_alpha()
        self.login= pygame.transform.scale(self.login, (170, 70))

        self.game = pygame.image.load('asset/image/ui/game.png').convert_alpha()
        self.game = pygame.transform.scale(self.game, (250, 120))

        self.setting = pygame.image.load('asset/image/ui/setting.png').convert_alpha()
        self.setting = pygame.transform.scale(self.setting, (240, 110))

        self.stop = pygame.image.load('asset/image/ui/stop.png').convert_alpha()
        self.stop = pygame.transform.scale(self.stop, (240, 120))

        # Luu anh va vi tri cac nut
        self.buttons = [
            [self.game, self.game.get_rect(center=(400, 490)), "PLAY"],
            [self.setting, self.setting.get_rect(center=(400, 570)), "SETTING"],
            [self.stop, self.stop.get_rect(center=(400, 650)), "EXIT"],
            [self.login, self.login.get_rect(center=(150, 650)), "LOGIN"]
        ]

    def run(self):
        self.screen.blit(self.nen, (-270, 0))

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
