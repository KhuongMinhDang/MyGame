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

        # Luu anh va vi tri cac nut
        self.buttons = [
            [self.game, self.game.get_rect(center=(400, 610)), "PLAY"],
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
