import pygame


class char_select:
    def __init__(self, screen):
        self.screen = screen

        # 4 o boss
        self.bosses = []
        for i in range(4):
            image = pygame.Surface((250, 130))
            image.fill('gray')

            rect = image.get_rect(
                center=(
                    250 + (i % 2) * 300,
                    150 + (i // 2) * 160
                )
            )

            self.bosses.append((image, rect))

        # 4 may bay
        self.players = []

        for i in range(1, 5):
            image = pygame.image.load(
                f"asset/image/SpaceShips/Ship_{i}.png"
            ).convert_alpha()

            small = pygame.transform.scale(image, (100, 70))
            big = pygame.transform.scale(image, (140, 100))

            rect = small.get_rect(
                center=(140 + (i - 1) * 175, 500)
            )

            self.players.append((small, big, rect))

        # Nut PLAY
        self.play_image = pygame.Surface((150, 60))
        self.play_image.fill('green')

        self.play_rect = self.play_image.get_rect(
            center=(400, 650)
        )

    def run(self):

        # Ve 4 boss
        for image, rect in self.bosses:
            self.screen.blit(image, rect)

        # Ve 4 may bay
        mouse_pos = pygame.mouse.get_pos()

        for small, big, rect in self.players:

            if rect.collidepoint(mouse_pos):
                image = big
                draw_rect = image.get_rect(center=rect.center)
            else:
                image = small
                draw_rect = rect

            self.screen.blit(image, draw_rect)

        # Ve nut PLAY
        self.screen.blit(self.play_image, self.play_rect)