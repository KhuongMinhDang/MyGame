import pygame

class Explosion(pygame.sprite.Sprite):
    frames = [] # Bộ nhớ đệm để không phải tải lại ảnh nhiều lần
    def __init__(self, x, y):
        super().__init__()
        if not Explosion.frames:
            for i in range(10):
                img = pygame.image.load(f"asset/image/ui/exp_{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (100,100)) 
                Explosion.frames.append(img)
        self.current_frame = 0
        self.image = Explosion.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # Tốc độ lật ảnh (50 mili-giây/frame)
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame < len(Explosion.frames):
                self.image = Explosion.frames[self.current_frame]
            else:
                self.kill()