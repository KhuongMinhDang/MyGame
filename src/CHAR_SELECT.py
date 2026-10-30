import pygame


class char_select:
    def __init__(self, screen):
        self.screen = screen
        # 2 o boss
        self.bosses = []
        self.selected_boss = 0
        for i in range(1, 4):
            image = pygame.image.load(f"asset/image/SpaceShips/boss{i}.png").convert_alpha()

            small = pygame.transform.scale(image, (250, 190))
            big = pygame.transform.scale(image, (380, 300))

            rect = small.get_rect(center=(120 + (i - 1) * 270, 200))

            self.bosses.append((small, big, rect))
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
        self.back =pygame.image.load('asset/image/ui/back-3.png').convert_alpha()
        self.back = pygame.transform.scale(self.back, (150, 60))
        self.back_rect = self.back.get_rect(center=(720, 40))

        self.play_image = pygame.image.load('asset/image/ui/game-3.png').convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, (150, 60))
        self.play_rect = self.play_image.get_rect(center=(400, 650))
        #man hinh
        self.background = pygame.image.load('asset/image/ui/background.jpg').convert_alpha()
        self.background= pygame.transform.scale(self.background, (800, 750))
    def run(self):
        self.screen.blit(self.background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        # Ve 3 boss
        for i, (small, big, rect) in enumerate(self.bosses):
            if rect.collidepoint(mouse_pos):
                image = big
                draw_rect = image.get_rect(center=rect.center)
            else:
                image = small
                draw_rect = rect

            self.screen.blit(image, draw_rect)

            # Tam giac chi vao boss dang chon
            if i == self.selected_boss:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 255),
                    [
                        (rect.centerx - 8, rect.top - 20),
                        (rect.centerx + 8, rect.top - 20),
                        (rect.centerx, rect.top - 5)
                    ]
                )

        # Ve 4 may bay

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
