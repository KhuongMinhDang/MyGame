import pygame
from random import choice
from src.Giao_dien import giao_dien
from src.Player import player
from src.obstacle import obstacle
from src.Bullet import Bullet, LaserBeam
from src.Sound import sound
from src.CHAR_SELECT import char_select
from src.Background import Background
pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 750))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MY GAME")

        self.menu = giao_dien(self.screen)
        self.state = "MENU"
        # them nguoi choi
        self.player = pygame.sprite.GroupSingle()
        self.player.add(player(0))
        #background
        self.background = Background()
        ##### them quai
        self.SPAWM = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWM, 300)
        self.Quai = pygame.sprite.Group()
        #am thanh
        self.sound = sound()
        #####bullet
        self.bullet = pygame.sprite.Group()
        self.SPAWM_bullet = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWM_bullet, 300)
        # Laser tu dong ban lien tuc
        self.laser = pygame.sprite.GroupSingle()
        self.laser.add(LaserBeam(self.player.sprite))
        # Che do vu khi: "LASER" (mac dinh) hoac "BULLET" (Nhan phim 1 / 2 de doi)
        self.weapon_type = "LASER"
        #chon nhan vat
        self.char_select = char_select(self.screen)
        # Biến này để kiểm soát vòng lặp game, thay cho biến running cục bộ
        self.running = True

    def su_kien_menu(self, event):
        """Hàm xử lý riêng các click chuột khi đang ở MENU"""
        if self.menu.buttons[0][0].collidepoint(event.pos):
            print("Chuyển sang màn hình chọn nhân vật!")
            self.state = "CHAR_SELECT"  # Cập nhật trạng thái!

        elif self.menu.buttons[1][0].collidepoint(event.pos):
            print("Mở Setting")

        elif self.menu.buttons[2][0].collidepoint(event.pos):
            print("Exit")
            self.running = False  # Tắt game

    def su_kien_char_select(self, event):
        if self.char_select.play_rect.collidepoint(event.pos):
            self.state = "PLAY"
        for i in range(4):
            if self.char_select.players[i][2].collidepoint(event.pos):
                self.char_select.selected = i
                self.player.add(player(i))
                self.laser.add(LaserBeam(self.player.sprite))
                break

    #va cham
    def va_cham(self):
        ds_va_cham = pygame.sprite.spritecollide(self.player.sprite, self.Quai, True)
        if ds_va_cham:
            self.sound.play_explosion()
            #self.running=False

    def ban_dan(self):
        # 1. Đạn thường bắn trúng quái
        ds = pygame.sprite.groupcollide(self.bullet, self.Quai, True, True)
        if ds:
            self.sound.play_explosion()

        # 2. Tia Laze quét trúng quái 
        if self.weapon_type == "LASER" and self.laser.sprite:
            ds_laser = pygame.sprite.spritecollide(self.laser.sprite, self.Quai, True)
            if ds_laser:
                self.sound.play_explosion()

    def run_game(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            # --- 1. PHẦN XỬ LÝ SỰ KIỆN CHUỘT/BÀN PHÍM ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # 1: Đạn thường,2: Laser
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.weapon_type = "BULLET"
                    elif event.key == pygame.K_2:
                        self.weapon_type = "LASER"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Chuyển hướng sự kiện tùy theo trạng thái game
                    if self.state == "MENU": self.su_kien_menu(event)
                    if self.state == "CHAR_SELECT": self.su_kien_char_select(event)

                if self.state == "PLAY":
                    if event.type == self.SPAWM:
                        self.Quai.add(obstacle(choice(["down", "sin"])))
                    if event.type == self.SPAWM_bullet and self.weapon_type == "BULLET":
                        self.sound.play_shot()
                        self.bullet.add(Bullet(self.player.sprite))

            # --- 2. PHẦN CẬP NHẬT LOGIC VÀ VẼ LÊN MÀN HÌNH ---
            if self.state == "MENU":
                self.menu.run()  # Vẽ giao diện Menu

            elif self.state == "CHAR_SELECT":
                self.char_select.run()
            else:
                self.background.update()
                self.background.draw(self.screen)
                self.player.update()
                self.player.draw(self.screen)
                self.Quai.update()
                self.Quai.draw(self.screen)
                self.va_cham()

                # Cập nhật và vẽ vũ khí đang chọn
                if self.weapon_type == "LASER":
                    self.laser.update()
                    self.laser.draw(self.screen)
                else:
                    self.bullet.update()
                    self.bullet.draw(self.screen)

                self.ban_dan()


            # --- 3. CẬP NHẬT FRAME ---
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
