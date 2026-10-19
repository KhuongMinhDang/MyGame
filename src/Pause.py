import pygame
class Pause:
    def __init__(self,screen):
        self.screen = screen
        self.surface = pygame.Surface((300, 250), pygame.SRCALPHA)
        self.surface.fill((20, 20, 40, 220))
        self.resume = pygame.image.load("asset/image/ui/resume.png").convert_alpha();
        self.resume = pygame.transform.scale(self.resume, (190, 100))
        self.restart = pygame.image.load("asset/image/ui/restart.png").convert_alpha();
        self.restart = pygame.transform.scale(self.restart, (190, 100))
        self.main_menu= pygame.image.load("asset/image/ui/main_menu.png").convert_alpha();
        self.main_menu = pygame.transform.scale(self.main_menu, (190, 100))
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