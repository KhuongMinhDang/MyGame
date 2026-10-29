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
        #ket qua hien thi
        self.screen = screen
        self.font=pygame.font.Font("asset/image/ui/font.ttf", 40)
        self.result_now=None
        self.screen=screen

        self.restart = pygame.image.load("asset/image/ui/restart-3.png").convert_alpha();
        self.restart = pygame.transform.scale(self.restart, (150, 60))
        self.main_menu = pygame.image.load("asset/image/ui/main_menu-3.png").convert_alpha();
        self.main_menu = pygame.transform.scale(self.main_menu, (150, 60))
        self.buttons = [
            [self.restart, self.restart.get_rect(center=(300, 370)), "restart"],
            [self.main_menu, self.main_menu.get_rect(center=(500, 370)), "main_menu"]
        ]
    def update(self):
        if(not self.result_now=="Win"):
            text = self.font.render("YOU LOSE", True, (255, 0, 0))

            rect = text.get_rect(center=(400, 300))

            self.screen.blit(text, rect)
        else:
            text = self.font.render("YOU WIN", True, (255, 0, 0))

            rect = text.get_rect(center=(400, 300))

            self.screen.blit(text, rect)

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
