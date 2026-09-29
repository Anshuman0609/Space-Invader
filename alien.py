import os
import random
from PIL import Image, ImageTk
import settings as s

_SPRITE_CACHE = {}

def get_sprite_image(filename: str, width: int, height: int):
    key = (filename, width, height)
    if key in _SPRITE_CACHE:
        return _SPRITE_CACHE[key]

    path = os.path.join(s.ASSETS_DIR, filename)
    if os.path.exists(path):
        try:
            pil_img = Image.open(path).convert("RGBA")
            resized = pil_img.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            _SPRITE_CACHE[key] = photo
            return photo
        except Exception:
            pass
    return None

class Alien:
    def __init__(self, canvas, x: float, y: float, row_idx: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.alive = True
        self.width = s.ALIEN_WIDTH
        self.height = s.ALIEN_HEIGHT

        config = s.ALIEN_TYPES[row_idx]
        self.sprite_name = config["sprite"]
        self.points = config["points"]

        self.image = get_sprite_image(self.sprite_name, self.width, self.height)

        if self.image:
            self.shape_id = self.canvas.create_image(
                self.x, self.y, image=self.image, anchor="center"
            )
        else:
            hw = self.width / 2
            hh = self.height / 2
            self.shape_id = self.canvas.create_rectangle(
                self.x - hw, self.y - hh,
                self.x + hw, self.y + hh,
                fill="#FF00FF", outline="#FFFFFF"
            )

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self.canvas.move(self.shape_id, dx, dy)

    def get_bbox(self) -> tuple[float, float, float, float]:
        hw = self.width / 2
        hh = self.height / 2
        return (self.x - hw, self.y - hh, self.x + hw, self.y + hh)

    def destroy(self):
        self.alive = False
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
            self.shape_id = None

class AlienGrid:
    def __init__(self, canvas, wave: int = 1):
        self.canvas = canvas
        self.wave = wave
        self.aliens: list[Alien] = []
        self.direction = 1
        self.base_speed = s.ALIEN_BASE_SPEED + (wave - 1) * 0.25
        self.speed = self.base_speed
        self.shoot_chance = s.ALIEN_SHOOT_CHANCE + (wave - 1) * 0.0005
        self.total_aliens = 0

        self._spawn_fleet()

    def _spawn_fleet(self):
        for row in range(s.ALIEN_ROWS):
            for col in range(s.ALIEN_COLS):
                x = s.ALIEN_START_X + col * (s.ALIEN_WIDTH + s.ALIEN_SPACING_X)
                y = s.ALIEN_START_Y + row * (s.ALIEN_HEIGHT + s.ALIEN_SPACING_Y)
                alien = Alien(self.canvas, x, y, row)
                self.aliens.append(alien)

        self.total_aliens = len(self.aliens)

    def update(self):
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            return

        killed = self.total_aliens - len(alive_aliens)
        self.speed = self.base_speed + killed * s.ALIEN_SPEEDUP_PER_KILL

        hit_edge = False
        for alien in alive_aliens:
            if self.direction == 1 and (alien.x + alien.width / 2) >= s.SCREEN_WIDTH - 15:
                hit_edge = True
                break
            elif self.direction == -1 and (alien.x - alien.width / 2) <= 15:
                hit_edge = True
                break

        if hit_edge:
            self.direction *= -1
            for alien in alive_aliens:
                alien.move(0, s.ALIEN_DROP_STEP)
        else:
            dx = self.speed * self.direction
            for alien in alive_aliens:
                alien.move(dx, 0)

    def try_shoot(self) -> list[tuple[float, float]]:
        shots = []
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            return shots

        columns: dict[int, Alien] = {}
        col_width = s.ALIEN_WIDTH + s.ALIEN_SPACING_X
        for alien in alive_aliens:
            col_index = round(alien.x / col_width)
            if col_index not in columns or alien.y > columns[col_index].y:
                columns[col_index] = alien

        for alien in columns.values():
            if random.random() < self.shoot_chance:
                shots.append((alien.x, alien.y + alien.height / 2 + 4))

        return shots

    def get_lowest_y(self) -> float:
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            return 0
        return max(a.y + a.height / 2 for a in alive_aliens)

    def alive_count(self) -> int:
        return sum(1 for a in self.aliens if a.alive)

    def destroy_all(self):
        for alien in self.aliens:
            if alien.alive:
                alien.destroy()
        self.aliens.clear()
