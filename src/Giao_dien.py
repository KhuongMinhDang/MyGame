import pygame


class giao_dien:
    def __init__(self, screen):
        self.screen = screen

        # 1. Load và scale ảnh nền khớp với cửa sổ 800x800
        self.nen = pygame.image.load('asset/image/ui/giao_dien.png').convert_alpha()
        self.nen = pygame.transform.scale(self.nen, (800, 800))

        # 2. Load ảnh 2 trạng thái của nút
        self.button = pygame.image.load('asset/image/ui/Button.png').convert_alpha()
        self.button_a = pygame.image.load('asset/image/ui/Button-a.png').convert_alpha()
        self.button = pygame.transform.scale(self.button, (300, 50))
        self.button_a = pygame.transform.scale(self.button_a, (300, 50))
        # Vi tri cac button
        self.buttons = [(self.button.get_rect(center=(400, 450)), "PLAY"),
                        (self.button.get_rect(center=(400, 500)), "SETTING"),
                        (self.button.get_rect(center=(400, 550)), "EXIT")]
        # 3. Tạo font chữ để in lên nút
        self.font = pygame.font.SysFont("arial", 30, bold=True)


    def run(self):
        self.screen.blit(self.nen, (0, 0))

        pos=pygame.mouse.get_pos()
        for rect, text in self.buttons:
            if(rect.collidepoint(pos)):
                image=self.button_a
            else: image=self.button
            self.screen.blit(image,rect)
            text_image = self.font.render( text, True, (255, 255, 255) )
            self.screen.blit( text_image, text_image.get_rect(center=rect.center) )