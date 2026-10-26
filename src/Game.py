import pygame
from random import choice

from pygame.display import update

from src.Giao_dien import giao_dien
from src.Player import player
from src.Bullet import bullet_list
from src.Sound import sound
from src.CHAR_SELECT import char_select
from src.Background import Background
from src.Boss import Boss
from src.BossBullet import boss_bullet_list
from src.Pause import Pause
pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 750))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MY GAME")
        #pause
        self.Pause = Pause(self.screen)

        self.menu = giao_dien(self.screen)
        self.state = "MENU"
        # them nguoi choi (mac dinh la player 0)
        self.selected_player_id = 0
        self.player = pygame.sprite.GroupSingle()
        self.player.add(player(self.selected_player_id))
        #background
        self.background = Background()
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

        self.char_select = char_select(self.screen)
        # chon boss
        self.boss_group = pygame.sprite.GroupSingle()
        self.boss_group.add(Boss(2))
        # Biến này để kiểm soát vòng lặp game, thay cho biến running cục bộ
        self.running = True
        #luu lai man hinh
        self.pause_background = None

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
        for i in range(2):
            if self.char_select.bosses[i][2].collidepoint(event.pos):
                self.char_select.selected_boss=i;
                self.boss_group.add(Boss(i));
                break;

    def restart_game(self):
        # Dat lai nguoi choi
        self.player.empty()
        self.player.add(player(self.selected_player_id))
        # Xoa dan cu
        self.bullet.empty()
        self.laser.empty()
        # Tao lai boss
        self.boss_group.empty()
        self.boss_group.add(Boss(self.char_select.selected_boss))
        # Dat lai background
        self.background = Background()
        # Cap nhat vu khi theo nhan vat hien tai
        self.cap_nhat_vu_khi(self.selected_player_id)
        # Chuyen ve man choi
        if(self.state=="PAUSE"): self.state = "PLAY"
    def su_kien_pause(self,event):
        if self.background.nut_pause_rect.collidepoint(event.pos) and self.state=="PLAY":
            self.state = "PAUSE"
        if self.state=="PAUSE":
            if self.Pause.buttons[0][1].collidepoint(event.pos):
                self.state = "PLAY"
            if self.Pause.buttons[1][1].collidepoint(event.pos):
                self.restart_game()
            if self.Pause.buttons[2][1].collidepoint(event.pos):
                self.state = "CHAR_SELECT"

    def trung_boss(self):
        boss = self.boss_group.sprite

        if boss is None:
            return
        dan_trung = pygame.sprite.spritecollide(boss, self.bullet, True,collided=lambda bo, d: bo.hitbox.colliderect(d.rect))
        for dan in dan_trung:
            boss.luong_mau(dan.damage)
            print("Boss HP:", boss.hp)  # DEBUG: xoá khi xong
            # Laser: trúng thì KHÔNG xoá (False), trừ máu mỗi frame
        for tia in pygame.sprite.spritecollide(boss, self.laser, False, collided=lambda bo, d: bo.hitbox.colliderect(d.rect)):
            boss.luong_mau(tia.damage)
            print("Boss HP:", boss.hp)  # DEBUG: xoá khi xong
    #va cham
    def va_cham(self):
        for boss in self.boss_group:
            # Tham số True ở cuối có nghĩa là: Khi đạn chạm vào Player, viên đạn đó sẽ tự động biến mất (bị kill)
            dan_trung_player = pygame.sprite.spritecollide(self.player.sprite, boss.bullets, True,
                collided=lambda p, b: p.hitbox.colliderect(b.hitbox))
            if dan_trung_player:
                #if(self.player.sprite.current_hp+1>3):
                    #self.state = "CHAR_SELECT"
                    #self.player.sprite.current_hp=0
                   # self.restart_game()
                #else:
                   # self.player.sprite.current_hp+=1
                    self.sound.play_explosion()
                    print("dinhdan")
                    #self.running=False

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
                    if self.state == "PLAY": self.su_kien_pause(event)
                    if self.state == "PAUSE": self.su_kien_pause(event)
                if self.state == "PLAY":
                    weapon_cls = bullet_list[self.selected_player_id]
                    #chi boss xh moi ban
                    boss = self.boss_group.sprite
                    if event.type == self.SPAWM_bullet and weapon_cls.kind == "BULLET" and boss is not None and not boss.dang_bay:
                        self.sound.play_shot()
                        self.bullet.add(weapon_cls(self.player.sprite))
                    #nhan pause
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "PAUSE"

            # --- 2. PHẦN CẬP NHẬT LOGIC VÀ VẼ LÊN MÀN HÌNH ---
            if self.state == "MENU":
                self.menu.run()  # Vẽ giao diện Menu

            elif self.state == "CHAR_SELECT":
                self.char_select.run()
            elif self.state == "PLAY":
                self.background.update()
                self.background.draw(self.screen)

                self.player.update(self.screen)
                self.player.draw(self.screen)
                pygame.draw.rect(self.screen, (255, 0, 0), self.player.sprite.hitbox, 1)

                self.boss_group.update(self.player.sprite)
                self.boss_group.draw(self.screen)
                for boss in self.boss_group:
                    boss.bullets.update()       
                    boss.bullets.draw(self.screen)
                    boss.explosions_group.draw(self.screen) #vu no
                self.va_cham()
                self.trung_boss()
                # DEBUG: xoá khi chỉnh xong
                pygame.draw.rect(self.screen, (255, 0, 0), self.player.sprite.hitbox, 1)
                for boss in self.boss_group:
                    pygame.draw.rect(self.screen, (255, 255, 0), boss.hitbox, 1)
                    for b in boss.bullets:
                        pygame.draw.rect(self.screen, (0, 255, 0), b.hitbox, 1)
                boss = self.boss_group.sprite
                if boss:
                    ty_le = max(boss.hp, 0) / boss.max_hp
                    pygame.draw.rect(self.screen, (80, 0, 0), (150, 10, 500, 10))
                    pygame.draw.rect(self.screen, (255, 0, 0), (150, 10, 500 * ty_le, 10))
                # Cập nhật và vẽ vũ khí tương ứng của player[i]
                weapon_cls = bullet_list[self.selected_player_id]
                if weapon_cls.kind == "LASER":
                    self.laser.update()
                    self.laser.draw(self.screen)
                else:
                    self.bullet.update()
                    self.bullet.draw(self.screen)

                self.pause_background = self.screen.copy()
            elif self.state == "PAUSE":
                if self.pause_background is not None:
                    self.screen.blit(self.pause_background, (0, 0))
                self.Pause.update()


            # --- 3. CẬP NHẬT FRAME ---
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
