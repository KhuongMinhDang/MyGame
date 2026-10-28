import pygame
import random
from random import choice

from src.Giao_dien import giao_dien
from src.Player import player
from src.Bullet import bullet_list
from src.Sound import sound
from src.CHAR_SELECT import char_select
from src.Background import Background
from src.Boss import Boss
from src.BossBullet import boss_bullet_list
from src.Pause import Pause, Result
from src.Item import Item
pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 750))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MY GAME")
        #pause
        self.Pause = Pause(self.screen)
        #result
        self.result= Result(self.screen)
        #giao dien
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
        #####bullet player
        self.bullet = pygame.sprite.Group()
        self.SPAWM_bullet = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWM_bullet, 300)
        # Laser
        self.laser = pygame.sprite.GroupSingle()

        # Vat pham: xuat hien ngau nhien moi 15 giay (15000 ms)
        self.item_group = pygame.sprite.Group()
        self.SPAWN_ITEM = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SPAWN_ITEM, 15000)
        self.hud_font = pygame.font.SysFont("arial", 15, bold=True)

        # Gan loai dan bullet_list[0] tuong ung voi player 0
        self.cap_nhat_vu_khi(self.selected_player_id)

        self.char_select = char_select(self.screen)
        # chon boss
        self.boss_chet_luc = None  # thoi diem boss het mau
        self.boss_group = pygame.sprite.GroupSingle()
        self.boss_group.add(Boss(0))
        # Biến này để kiểm soát vòng lặp game, thay cho biến running cục bộ
        self.running = True
        #luu lai man hinh
        self.pause_background = None
        #bat hitbox
        self.hitbox=False
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
            self.item_group.empty()
            pygame.time.set_timer(self.SPAWN_ITEM, 15000)
        for i in range(4):
            if self.char_select.players[i][2].collidepoint(event.pos):
                self.char_select.selected = i
                self.player.add(player(i))
                # Khi chon player[i], tu dong gan dan bullet_list[i]
                self.cap_nhat_vu_khi(i)
                break
        if self.char_select.back_rect.collidepoint(event.pos):
            self.state = "MENU"
        for i in range(3):
            if self.char_select.bosses[i][2].collidepoint(event.pos):
                self.char_select.selected_boss=i;
                self.boss_group.add(Boss(i));
                break;

    def restart_game(self):
        #dat lai hp boss
        self.boss_chet_luc = None  # thoi diem boss het mau
        # Dat lai nguoi choi
        self.player.empty()
        self.player.add(player(self.selected_player_id))
        # Xoa dan cu
        self.bullet.empty()
        self.laser.empty()
        # Xoa vat pham cu va reset timer spawn vat pham
        self.item_group.empty()
        pygame.time.set_timer(self.SPAWN_ITEM, 15000)
        # Tao lai boss
        self.boss_group.empty()
        self.boss_group.add(Boss(self.char_select.selected_boss))
        # Dat lai background
        self.background = Background()
        # Cap nhat vu khi theo nhan vat hien tai
        self.cap_nhat_vu_khi(self.selected_player_id)
        # Chuyen ve man choi
        if(self.state== "PAUSE" ): self.state = "PLAY"
        if(self.state== "RESULT" ): self.state = "PLAY"
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
                self.restart_game()

    def trung_boss(self):
        boss = self.boss_group.sprite

        if boss is None:
            return

        now = pygame.time.get_ticks()
        multiplier = 2 if (self.player.sprite and self.player.sprite.is_double_damage(now)) else 1

        dan_trung = pygame.sprite.spritecollide(boss, self.bullet, True, collided=lambda bo, d: bo.hitbox.colliderect(d.rect))
        for dan in dan_trung:
            boss.luong_mau(getattr(dan, 'damage', 10) * multiplier)
            print("Boss HP:", boss.hp)
            # Laser: trúng thì KHÔNG xoá (False), trừ máu mỗi frame
        for tia in pygame.sprite.spritecollide(boss, self.laser, False, collided=lambda bo, d: bo.hitbox.colliderect(d.rect)):
            boss.luong_mau(getattr(tia, 'damage', 1) * multiplier)
            print("Boss HP:", boss.hp)

        # Boss het mau -> cho no xong roi moi hien Win
        if boss.hp <= 0:
            if self.boss_chet_luc is None:
                self.boss_chet_luc = now  # bat dau dem gio
            elif now - self.boss_chet_luc >= 1500:  # 2 giay, chinh theo do dai vu no
                self.boss_chet_luc = None
                if self.state == "PLAY":
                    self.result.result_now = "Win"
                    self.state = "RESULT"
    #va cham
    def va_cham(self):
        boss = self.boss_group.sprite
        if boss is not None and boss.hp <= 0:
            return  # boss dang no, khong tinh va cham nua
        now = pygame.time.get_ticks()
        is_inv = self.player.sprite and self.player.sprite.is_invincible(now)
        for boss in self.boss_group:
            # Tham số True ở cuối có nghĩa là: Khi đạn chạm vào Player, viên đạn đó sẽ tự động biến mất (bị kill)
            dan_trung_player = pygame.sprite.spritecollide(self.player.sprite, boss.bullets, True,
                collided=lambda p, b: p.hitbox.colliderect(b.hitbox))
            if dan_trung_player:
                self.sound.play_explosion()
                if is_inv:
                    print("Khien bao ve chan dan Boss! Bat tu, khong mat mau.")
                else:
                    self.result.result_now="Loser"
                    self.state="RESULT"
                    print("dinhdan")
                    #self.running=False

    def nhat_vat_pham(self):
        """Xử lý máy bay di chuyển đến vị trí vật phẩm thì nhận hiệu ứng"""
        if not self.player.sprite:
            return
        now = pygame.time.get_ticks()
        items_hit = pygame.sprite.spritecollide(
            self.player.sprite,
            self.item_group,
            True,
            collided=lambda p, itm: p.rect.colliderect(itm.rect)
        )
        for item in items_hit:
            if item.item_type == "DOUBLE_DAMAGE":
                self.player.sprite.activate_double_damage(now, 10000)
                print("Nhat vat pham: X2 SAT THUONG trong 10 giay!")
            elif item.item_type == "SHIELD":
                self.player.sprite.activate_invincible(now, 10000)
                print("Nhat vat pham: BAT TU trong 10 giay!")

    def ve_hud_buff(self):
        """Hiển thị thời gian đếm ngược của các hiệu ứng vật phẩm đang kích hoạt"""
        if not self.player.sprite:
            return
        now = pygame.time.get_ticks()
        y_offset = 35

        # Hiển thị HUD Khiên Bất Tử
        if self.player.sprite.is_invincible(now):
            remain_sec = (self.player.sprite.invincible_until - now) / 1000.0
            surf = pygame.Surface((180, 26), pygame.SRCALPHA)
            surf.fill((0, 40, 80, 190))
            ratio = max(0.0, min(1.0, remain_sec / 10.0))
            pygame.draw.rect(surf, (0, 180, 255, 140), (2, 2, int(176 * ratio), 22), border_radius=4)
            pygame.draw.rect(surf, (0, 230, 255), (0, 0, 180, 26), 2, border_radius=5)
            self.screen.blit(surf, (15, y_offset))
            txt = self.hud_font.render(f"SHIELD: {remain_sec:.1f}s", True, (255, 255, 255))
            self.screen.blit(txt, (25, y_offset + 5))
            y_offset += 32

        # Hiển thị HUD X2 Sát Thương
        if self.player.sprite.is_double_damage(now):
            remain_sec = (self.player.sprite.double_damage_until - now) / 1000.0
            surf = pygame.Surface((180, 26), pygame.SRCALPHA)
            surf.fill((80, 30, 0, 190))
            ratio = max(0.0, min(1.0, remain_sec / 10.0))
            pygame.draw.rect(surf, (255, 100, 0, 160), (2, 2, int(176 * ratio), 22), border_radius=4)
            pygame.draw.rect(surf, (255, 140, 0), (0, 0, 180, 26), 2, border_radius=5)
            self.screen.blit(surf, (15, y_offset))
            txt = self.hud_font.render(f"2X DAMAGE: {remain_sec:.1f}s", True, (255, 255, 255))
            self.screen.blit(txt, (25, y_offset + 5))
    def bang_result(self,event):

        if(self.result.buttons[0][1].collidepoint(event.pos)):
            self.restart_game()
            self.result.result_now="None"
        if(self.result.buttons[1][1].collidepoint(event.pos)):
            self.result.result_now="None"
            self.state = "CHAR_SELECT"
            self.restart_game()
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
                    if self.state == "RESULT": self.bang_result(event)
                if self.state == "PLAY":
                    weapon_cls = bullet_list[self.selected_player_id]
                    #chi boss xh moi ban
                    boss = self.boss_group.sprite
                    if event.type == self.SPAWM_bullet and weapon_cls.kind == "BULLET" and boss is not None and not boss.dang_bay:
                        self.sound.play_shot()
                        self.bullet.add(weapon_cls(self.player.sprite))
                    # Xuất hiện vật phẩm ngẫu nhiên mỗi 15 giây
                    if event.type == self.SPAWN_ITEM:
                        item_type = choice(["DOUBLE_DAMAGE", "SHIELD"])
                        spawn_x = random.randint(80, 720)
                        spawn_y = random.randint(50, 150)
                        self.item_group.add(Item(spawn_x, spawn_y, item_type))
                    #nhan pause
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "PAUSE"
                        if event.key == pygame.K_F1:
                            if self.hitbox: self.hitbox = False
                            else: self.hitbox = True

            # --- 2. PHẦN CẬP NHẬT LOGIC VÀ VẼ LÊN MÀN HÌNH ---
            if self.state == "MENU":
                self.menu.run()  # Vẽ giao diện Menu

            elif self.state == "CHAR_SELECT":
                self.char_select.run()
            elif self.state == "PLAY":
                self.background.update()
                self.background.draw(self.screen)

                # Cập nhật, vẽ và kiểm tra nhặt vật phẩm
                self.item_group.update()
                self.item_group.draw(self.screen)
                self.nhat_vat_pham()

                self.player.update(self.screen)
                self.player.draw(self.screen)

                self.boss_group.update(self.player.sprite)
                self.boss_group.draw(self.screen)
                for boss in self.boss_group:
                    boss.bullets.update()
                    boss.bullets.draw(self.screen)
                    boss.explosions_group.draw(self.screen) #vu no
                self.va_cham()
                self.trung_boss()
                # nhan F11 de hien hitbox
                if(self.hitbox==True):
                    pygame.draw.rect(self.screen, (255, 0, 0), self.player.sprite.hitbox, 1)
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
                    self.sound.play_shot()
                    self.laser.update()
                    self.laser.draw(self.screen)
                else:
                    self.bullet.update()
                    self.bullet.draw(self.screen)

                # Vẽ HUD đếm ngược hiệu ứng buff
                self.ve_hud_buff()

                self.pause_background = self.screen.copy()
            elif self.state == "PAUSE":
                if self.pause_background is not None:
                    self.screen.blit(self.pause_background, (0, 0))
                self.Pause.update()
            elif self.state == "RESULT":
                if self.result.result_now=="Win":
                    if self.pause_background is not None:
                        self.screen.blit(self.pause_background, (0, 0))
                    self.result.update()
                else:
                    self.result.update()

            # --- 3. CẬP NHẬT FRAME ---
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
