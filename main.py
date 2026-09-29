import random
import tkinter as tk
import settings as s
from player import Player
from alien import AlienGrid
from bullet import Bullet

class Game:
    STATE_TITLE = "title"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.running = True
        self.state = self.STATE_TITLE
        self.keys = set()

        self.score = 0
        self.lives = s.PLAYER_LIVES
        self.wave = 1
        self.shoot_cooldown = 0

        self.player = None
        self.alien_grid = None
        self.player_bullets = []
        self.alien_bullets = []

        self._overlay_items = []
        self._init_hud()
        self._init_stars()

        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

        self._show_title_screen()
        self._game_loop()

    def _on_key_press(self, event):
        self.keys.add(event.keysym)

    def _on_key_release(self, event):
        self.keys.discard(event.keysym)

    def _init_hud(self):
        self.score_text = self.canvas.create_text(
            20, 20, text="SCORE: 0", fill=s.COLOR_TEXT,
            font=(s.FONT_FAMILY, s.FONT_SMALL, "bold"), anchor="nw"
        )
        self.wave_text = self.canvas.create_text(
            s.SCREEN_WIDTH // 2, 20, text="WAVE: 1", fill="#AAAAAA",
            font=(s.FONT_FAMILY, s.FONT_SMALL, "bold"), anchor="n"
        )
        self.lives_text = self.canvas.create_text(
            s.SCREEN_WIDTH - 20, 20, text=f"LIVES: {s.PLAYER_LIVES}", fill=s.COLOR_PLAYER,
            font=(s.FONT_FAMILY, s.FONT_SMALL, "bold"), anchor="ne"
        )
        self.hud_line = self.canvas.create_line(
            0, 45, s.SCREEN_WIDTH, 45, fill="#333333", width=1
        )

    def _update_hud(self):
        self.canvas.itemconfigure(self.score_text, text=f"SCORE: {self.score}")
        self.canvas.itemconfigure(self.wave_text, text=f"WAVE: {self.wave}")
        self.canvas.itemconfigure(self.lives_text, text=f"LIVES: {self.lives}")

    def _set_hud_visible(self, visible: bool):
        state = "normal" if visible else "hidden"
        for item in (self.score_text, self.wave_text, self.lives_text, self.hud_line):
            self.canvas.itemconfigure(item, state=state)

    def _init_stars(self):
        for _ in range(70):
            x = random.randint(0, s.SCREEN_WIDTH)
            y = random.randint(0, s.SCREEN_HEIGHT)
            size = random.randint(1, 2)
            star_id = self.canvas.create_oval(x, y, x + size, y + size, fill=s.COLOR_STAR, outline="")
            self.canvas.tag_lower(star_id)

    def _show_title_screen(self):
        self.state = self.STATE_TITLE
        self._clear_overlay()
        self._set_hud_visible(False)

        cx = s.SCREEN_WIDTH // 2
        cy = s.SCREEN_HEIGHT // 2

        self._overlay_items.append(self.canvas.create_text(
            cx, cy - 80, text="SPACE INVADERS",
            fill=s.COLOR_PLAYER, font=(s.FONT_FAMILY, s.FONT_LARGE, "bold")
        ))
        self._overlay_items.append(self.canvas.create_text(
            cx, cy - 20, text="— Arcade Game —",
            fill="#888888", font=(s.FONT_FAMILY, s.FONT_SMALL)
        ))
        self._overlay_items.append(self.canvas.create_text(
            cx, cy + 30, text="Press [ ENTER ] to Start",
            fill=s.COLOR_TEXT, font=(s.FONT_FAMILY, s.FONT_MEDIUM, "bold")
        ))
        self._overlay_items.append(self.canvas.create_text(
            cx, cy + 90,
            text="\u2190 \u2192 Move   |   SPACE Shoot   |   ESC Quit",
            fill="#666666", font=(s.FONT_FAMILY, s.FONT_SMALL)
        ))

    def _start_new_game(self):
        self._clear_overlay()
        self._cleanup_entities()
        self._set_hud_visible(True)

        self.score = 0
        self.lives = s.PLAYER_LIVES
        self.wave = 1
        self.shoot_cooldown = 0
        self._update_hud()

        self.player = Player(self.canvas)
        self.alien_grid = AlienGrid(self.canvas, self.wave)

        self.state = self.STATE_PLAYING

    def _next_wave(self):
        self.wave += 1
        self._update_hud()

        for b in self.player_bullets:
            b.destroy()
        for b in self.alien_bullets:
            b.destroy()
        self.player_bullets.clear()
        self.alien_bullets.clear()

        self.alien_grid = AlienGrid(self.canvas, self.wave)

    def _game_over(self):
        self.state = self.STATE_GAME_OVER
        self._clear_overlay()

        cx = s.SCREEN_WIDTH // 2
        cy = s.SCREEN_HEIGHT // 2

        self._overlay_items.append(self.canvas.create_text(
            cx, cy - 70, text="GAME OVER",
            fill="#FF2222", font=(s.FONT_FAMILY, s.FONT_LARGE, "bold")
        ))
        self._overlay_items.append(self.canvas.create_text(
            cx, cy, text=f"Final Score: {self.score}",
            fill=s.COLOR_TEXT, font=(s.FONT_FAMILY, s.FONT_MEDIUM, "bold")
        ))
        self._overlay_items.append(self.canvas.create_text(
            cx, cy + 60, text="Press [ ENTER ] to Restart",
            fill=s.COLOR_PLAYER, font=(s.FONT_FAMILY, s.FONT_SMALL, "bold")
        ))

    def _clear_overlay(self):
        for item_id in self._overlay_items:
            self.canvas.delete(item_id)
        self._overlay_items.clear()

    def _game_loop(self):
        if not self.running:
            return

        if self.state == self.STATE_TITLE:
            if "Return" in self.keys:
                self.keys.discard("Return")
                self._start_new_game()

        elif self.state == self.STATE_PLAYING:
            self._handle_input()
            self._update_entities()
            self._check_collisions()

        elif self.state == self.STATE_GAME_OVER:
            if "Return" in self.keys:
                self.keys.discard("Return")
                self._cleanup_entities()
                self._start_new_game()

        if "Escape" in self.keys:
            self._quit()
            return

        self.canvas.after(s.GAME_SPEED_MS, self._game_loop)

    def _handle_input(self):
        if "Left" in self.keys:
            self.player.move(-1)
        if "Right" in self.keys:
            self.player.move(1)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if "space" in self.keys and self.shoot_cooldown <= 0:
            if len(self.player_bullets) < s.MAX_PLAYER_BULLETS:
                bx, by = self.player.get_nose_pos()
                bullet = Bullet(self.canvas, bx, by, s.PLAYER_BULLET_SPEED, s.COLOR_PLAYER_BULLET)
                self.player_bullets.append(bullet)
                self.shoot_cooldown = s.PLAYER_SHOOT_COOLDOWN

    def _update_entities(self):
        self.player.update()

        for bullet in self.player_bullets[:]:
            if not bullet.update():
                bullet.destroy()
                self.player_bullets.remove(bullet)

        self.alien_grid.update()

        for sx, sy in self.alien_grid.try_shoot():
            bullet = Bullet(self.canvas, sx, sy, s.ALIEN_BULLET_SPEED, s.COLOR_ALIEN_BULLET)
            self.alien_bullets.append(bullet)

        for bullet in self.alien_bullets[:]:
            if not bullet.update():
                bullet.destroy()
                self.alien_bullets.remove(bullet)

        if self.alien_grid.get_lowest_y() >= self.player.y - self.player.height // 2:
            self._game_over()

    def _check_collisions(self):
        for bullet in self.player_bullets[:]:
            bullet_box = bullet.get_bbox()
            hit_any = False

            for alien in self.alien_grid.aliens:
                if not alien.alive:
                    continue

                if self._check_overlap(bullet_box, alien.get_bbox()):
                    bullet.destroy()
                    self.player_bullets.remove(bullet)
                    alien.destroy()

                    self.score += alien.points
                    self._update_hud()

                    if self.alien_grid.alive_count() == 0:
                        self._next_wave()

                    hit_any = True
                    break

            if hit_any:
                continue

        if not self.player.is_invincible:
            player_box = self.player.get_bbox()
            for bullet in self.alien_bullets[:]:
                if self._check_overlap(player_box, bullet.get_bbox()):
                    bullet.destroy()
                    self.alien_bullets.remove(bullet)

                    self.lives -= 1
                    self._update_hud()

                    if self.lives <= 0:
                        self._game_over()
                    else:
                        self.player.respawn()
                    return

    @staticmethod
    def _check_overlap(box_a, box_b) -> bool:
        return (box_a[0] < box_b[2] and
                box_a[2] > box_b[0] and
                box_a[1] < box_b[3] and
                box_a[3] > box_b[1])

    def _cleanup_entities(self):
        if self.player:
            self.player.destroy()
            self.player = None
        if self.alien_grid:
            self.alien_grid.destroy_all()
            self.alien_grid = None
        for b in self.player_bullets:
            b.destroy()
        for b in self.alien_bullets:
            b.destroy()
        self.player_bullets.clear()
        self.alien_bullets.clear()

    def _quit(self):
        self.running = False
        self.root.destroy()

def main():
    root = tk.Tk()
    root.title(s.WINDOW_TITLE)
    root.resizable(False, False)

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - s.SCREEN_WIDTH) // 2
    y = (screen_h - s.SCREEN_HEIGHT) // 2
    root.geometry(f"{s.SCREEN_WIDTH}x{s.SCREEN_HEIGHT}+{x}+{y}")

    canvas = tk.Canvas(
        root,
        width=s.SCREEN_WIDTH,
        height=s.SCREEN_HEIGHT,
        bg=s.COLOR_BG,
        highlightthickness=0
    )
    canvas.pack()
    canvas.focus_set()

    game = Game(root, canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
