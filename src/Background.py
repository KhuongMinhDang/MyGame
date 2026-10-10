
import pygame
import random
class Background:
    def __init__(self):
        self.width = 800
        self.height = 750
        # Background tinh
        self.background=pygame.image.load("asset/image/Background/backgound.png").convert()
        self.background = pygame.transform.scale( self.background, (self.width, self.height) )
        #sao
        self.stars_y = 0
        self.stars_speed = 1
        self.space_stars=pygame.image.load("asset/image/Background/space-stars.png").convert_alpha()
        self.space_stars=pygame.transform.scale( self.space_stars, (self.width, self.height) )
        #cac hanh tinh
        self.planet_images=[]
        self.big_planet=pygame.image.load("asset/image/Background/big-planet.png").convert_alpha()
        self.far_planet =pygame.image.load("asset/image/Background/far-planets.png").convert_alpha()
        self.ring_planet =pygame.image.load("asset/image/Background/ring-planet.png").convert_alpha()
        self.planet_images.append(self.big_planet)
        self.planet_images.append(self.far_planet)
        self.planet_images.append(self.ring_planet)
        #danh sach hanh tinh xuat hien
        self.planets = []
        # Thoi gian spawn
        self.spawn_timer = 0
        self.spawn_delay = random.randint(60, 150)


    def spawn_planet(self):
        image = random.choice(self.planet_images)
        # Random kich thuoc
        size = random.randint(60, 180)
        image = pygame.transform.scale( image, (size, size) )
        # Random vi tri
        x = random.randint(0, self.width - size)
        # Random toc do
        speed = random.uniform(0.5, 2)
        planet = { "image": image, "x": x, "y": -size, "speed": speed }
        self.planets.append(planet)


    def update(self):
        #di chuyen sao
        self.stars_y += self.stars_speed
        if self.stars_y > self.height:
            self.stars_y = 0
        #thoi gian xuat hien cua cac ngoi sao
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_delay:
            self.spawn_planet()

            self.spawn_timer=0
            self.spawn_delay = random.randint(60, 150)
        #cho cac hanh tinh di chuyen
        for planet in self.planets:
            planet["y"]+=planet["speed"]
        #xoa cac hanh tinh roi khoi man hinh
        self.planets = [planet for planet in self.planets if planet["y"] < self.height]
    def draw(self,screen):
        # Ve background
        screen.blit(self.background, (0, 0))
        screen.blit(self.space_stars,(0,self.stars_y))
        screen.blit(self.space_stars,(0,self.stars_y-self.height))
        #cac hanh tinh
        for planet in self.planets:
            screen.blit(planet["image"],(planet["x"],planet["y"]))
