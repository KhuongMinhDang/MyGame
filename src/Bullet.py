import pygame
import math
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.image = pygame.Surface((10,15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=player.rect.midtop)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < -10:
            self.kill()


class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, player, base_width=14, color=(0, 240, 255)):
        
        super().__init__()
        self.player = player
        self.base_width = base_width
        self.color = color
        self.update()

    def update(self):
        
        beam_height = max(1, self.player.rect.top)

        ticks = pygame.time.get_ticks()
        pulse = math.sin(ticks * 0.02) * 2
        width = int(max(6, self.base_width + pulse))

        self.image = pygame.Surface((width, beam_height), pygame.SRCALPHA)

        outer_glow = (*self.color, 80)
        pygame.draw.rect(self.image, outer_glow, (0, 0, width, beam_height))

        inner_width = max(4, width // 2)
        inner_x = (width - inner_width) // 2
        inner_glow = (*self.color, 190)
        pygame.draw.rect(self.image, inner_glow, (inner_x, 0, inner_width, beam_height))

        core_width = max(2, width // 4)
        core_x = (width - core_width) // 2
        pygame.draw.rect(self.image, (255, 255, 255), (core_x, 0, core_width, beam_height))

        flare_radius = width // 2 + 3
        pygame.draw.circle(self.image, (255, 255, 255), (width // 2, beam_height - 2), flare_radius)
        pygame.draw.circle(self.image, (*self.color, 140), (width // 2, beam_height - 2), flare_radius + 4)

        self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)
