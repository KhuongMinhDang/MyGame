import pygame


class char_select:
    def __init__(self, screen):
        self.screen = screen
        # 4 o boss
        self.bosses = []
        for i in range(4):
            image = pygame.Surface((250, 130))
            image.fill('gray')

            rect = image.get_rect(center=(250 + (i % 2) * 300,150 + (i // 2) * 160))

            self.bosses.append((image, rect))

        # 4 may bay
        self.selected=0
        self.players = []
        for i in range(1, 5):
            image = pygame.image.load(f"asset/image/SpaceShips/Ship_{i}.png").convert_alpha()

            small = pygame.transform.scale(image, (100, 70))
            big = pygame.transform.scale(image, (140, 100))

            rect = small.get_rect(center=(140 + (i - 1) * 175, 500))

            self.players.append((small, big, rect))

        # Nut PLAY
        self.back =pygame.image.load('asset/image/ui/back.png').convert_alpha()
        self.back = pygame.transform.scale(self.back, (150, 70))
        self.back_rect = self.back.get_rect(center=(730, 40))

        self.play_image = pygame.image.load('asset/image/ui/game.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (200, 150))
        self.play_rect = self.play_image.get_rect(center=(400, 650))
        #man hinh
        self.background = pygame.image.load('asset/image/ui/background.webp').convert_alpha()
    def run(self):
        self.screen.blit(self.background, (0, 0))
        # Ve 4 boss
        for image, rect in self.bosses:
            self.screen.blit(image, rect)

        # Ve 4 may bay
        mouse_pos = pygame.mouse.get_pos()

        for i, (small, big, rect) in enumerate(self.players):

            if rect.collidepoint(mouse_pos):
                image = big
                draw_rect = image.get_rect(center=rect.center)
            else:
                image = small
                draw_rect = rect

            self.screen.blit(image, draw_rect)
            # Tam giac chi vao may bay dang chon
            if i == self.selected:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 255),
                    [
                        (rect.centerx - 8, rect.top - 20),
                        (rect.centerx + 8, rect.top - 20),
                        (rect.centerx, rect.top - 5)
                    ]
                )


        # Ve nut PLAY va BACK
        self.screen.blit(self.play_image, self.play_rect)
        self.screen.blit(self.back, self.back_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Hien mui ten khi tro chuot vao nut BACK
        if self.back_rect.collidepoint(mouse_pos):
            pygame.draw.polygon(
                self.screen,
                (255, 255, 255),
                [
                    (self.back_rect.left - 25, self.back_rect.centery - 10),
                    (self.back_rect.left - 25, self.back_rect.centery + 10),
                    (self.back_rect.left - 10, self.back_rect.centery)
                ]
            )

        # Hien mui ten khi tro chuot vao nut PLAY
        if self.play_rect.collidepoint(mouse_pos):
            pygame.draw.polygon(
                self.screen,
                (255, 255, 255),
                [
                    (self.play_rect.left - 25, self.play_rect.centery - 10),
                    (self.play_rect.left - 25, self.play_rect.centery + 10),
                    (self.play_rect.left - 10, self.play_rect.centery)
                ]
            )
