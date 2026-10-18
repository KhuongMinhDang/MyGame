import pygame
from random import choice
from src.Giao_dien import giao_dien
from src.Player import player
from src.obstacle import obstacle
from src.Bullet import bullet_list
from src.Sound import sound
from src.CHAR_SELECT import char_select
from src.Background import Background
from src.Boss import Boss
from src.BossBullet import boss_bullet_list
pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 750))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MY GAME")

        self.menu = giao_dien(self.screen)
        self.state = "MENU"
        # them nguoi choi (mac dinh la player 0)
        self.selected_player_id = 0
        self.player = pygame.sprite.GroupSingle()
        self.player.add(player(self.selected_player_id))
        #background
        self.background = Background()
        ##### them quai
        #self.SPAWM = pygame.USEREVENT + 1
        #pygame.time.set_timer(self.SPAWM, 300)
        self.Quai = pygame.sprite.Group()
        #am thanh
        self.sound = sound()
        #####bullet
        self.bullet = pygame.sprite.Group()
        self.SPAWM_bullet = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWM_bullet, 300)
        # Laser
        self.laser = pygame.sprite.GroupSingle()

        # Gan loai dan bullet_list[0] tuong ung voi player 0
        self.cap_nhat_vu_khi(self.selected_player_id)

        #chon nhan vat
        self.char_select = char_select(self.screen)
        self.boss_group = pygame.sprite.GroupSingle()
        self.boss_group.add(Boss(1))
        # Biến này để kiểm soát vòng lặp game, thay cho biến running cục bộ
        self.running = True

    def cap_nhat_vu_khi(self, ship_id):
        """player[i] se tu dong di chung voi bullet_list[i]"""
        self.selected_player_id = ship_id
        weapon_cls = bullet_list[ship_id]
        if weapon_cls.kind == "LASER":
            self.laser.empty()
            self.laser.add(weapon_cls(self.player.sprite))
        else:
            self.laser.empty()

    def su_kien_menu(self, event):
        """Hàm xử lý riêng các click chuột khi đang ở MENU"""
        if self.menu.buttons[0][1].collidepoint(event.pos):
            print("Chuyển sang màn hình chọn nhân vật!")
            self.state = "CHAR_SELECT"  # Cập nhật trạng thái!

        elif self.menu.buttons[1][1].collidepoint(event.pos):
            print("Mở Setting")

        elif self.menu.buttons[2][1].collidepoint(event.pos):
            print("Exit")
            self.running = False  # Tắt game

    def su_kien_char_select(self, event):
        if self.char_select.play_rect.collidepoint(event.pos):
            self.state = "PLAY"
        for i in range(4):
            if self.char_select.players[i][2].collidepoint(event.pos):
                self.char_select.selected = i
                self.player.add(player(i))
                # Khi chon player[i], tu dong gan dan bullet_list[i]
                self.cap_nhat_vu_khi(i)
                break
        if self.char_select.back_rect.collidepoint(event.pos):
            self.state = "MENU"

    #va cham
    def va_cham(self):
        ds_va_cham = pygame.sprite.spritecollide(self.player.sprite, self.Quai, True)
        if ds_va_cham:
            self.sound.play_explosion()
            #self.running=False
        for boss in self.boss_group:
            # Tham số True ở cuối có nghĩa là: Khi đạn chạm vào Player, viên đạn đó sẽ tự động biến mất (bị kill)
            dan_trung_player = pygame.sprite.spritecollide(self.player.sprite, boss.bullets, True)
            if dan_trung_player:
                print("dinhdan")
                #self.running=False

    def ban_dan(self):
        weapon_cls = bullet_list[self.selected_player_id]

        # 1. Đạn thường bắn trúng quái
        if weapon_cls.kind == "BULLET":
            ds = pygame.sprite.groupcollide(self.bullet, self.Quai, True, True)
            if ds:
                self.sound.play_explosion()

        # 2. Tia Laze quét trúng quái
        elif weapon_cls.kind == "LASER" and self.laser.sprite:
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

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Chuyển hướng sự kiện tùy theo trạng thái game
                    if self.state == "MENU": self.su_kien_menu(event)
                    if self.state == "CHAR_SELECT": self.su_kien_char_select(event)

                if self.state == "PLAY":
                    #if event.type == self.SPAWM:
                        #self.Quai.add(obstacle(choice(["down", "sin"])))
                    weapon_cls = bullet_list[self.selected_player_id]
                    if event.type == self.SPAWM_bullet and weapon_cls.kind == "BULLET":
                        self.sound.play_shot()
                        self.bullet.add(weapon_cls(self.player.sprite))

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

                #self.Quai.update()
                #self.Quai.draw(self.screen)
                if self.player.sprite:
                    self.boss_group.update(self.player.sprite)
                self.boss_group.draw(self.screen)
                for boss in self.boss_group:
                    boss.bullets.update()       
                    boss.bullets.draw(self.screen)

                self.va_cham()

                # Cập nhật và vẽ vũ khí tương ứng của player[i]
                weapon_cls = bullet_list[self.selected_player_id]
                if weapon_cls.kind == "LASER":
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
