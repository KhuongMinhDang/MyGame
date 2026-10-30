import pygame
class sound:
    def __init__(self):
        self.shot=pygame.mixer.Sound('asset/sound/audio_laser.ogg')
        self.shot.set_volume(0.05)
        self.explosion=pygame.mixer.Sound('asset/sound/audio_explosion.ogg')
        self.explosion.set_volume(0.5)
        self.win=pygame.mixer.Sound('asset/sound/win.ogg')
        self.win.set_volume(0.5)
    def play_shot(self):
        self.shot.play()
    def play_explosion(self):
        self.explosion.play()
    def play_win(self):
        self.win.play()