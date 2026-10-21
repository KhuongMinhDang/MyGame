import pygame


class player(pygame.sprite.Sprite):
    def __init__(self, x=0):
        super().__init__()
        self.ship_id = x
        #hp
        self.hp=[]
        self.current_hp=0
        for i in range(4):
            image=pygame.image.load(f"asset/image/ui/hp-{i}.png").convert_alpha()
            image=pygame.transform.scale(image, (70, 70))
            self.hp.append(image)
        # 1. Quản lý hình ảnh phi thuyền
        self.image_ship = [
            pygame.image.load('asset/image/SpaceShips/Ship_1.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_2.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_3.png').convert_alpha(),
            pygame.image.load('asset/image/SpaceShips/Ship_4.png').convert_alpha()
        ]
        self.image = self.image_ship[x]
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * 1.5), int(h * 1.5)))
        self.rect = self.image.get_rect(center=(400, 600))

    def update(self,screen):
        # 2. Quản lý chuyển động phi thuyền (WASD và Phím Mũi tên)
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.left <= 0: self.rect.left = 0
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.right >= 800: self.rect.right = 800
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= 3
            if self.rect.top <= 0: self.rect.top = 0
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += 3
            if self.rect.bottom >= 750: self.rect.bottom = 750
        # 2. Vẽ thanh HP góc dưới màn hình
        hp_image = self.hp[self.current_hp]
        screen.blit(hp_image, (0, 650))
