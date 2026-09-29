import os
from PIL import Image, ImageTk
import settings as s

class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = s.SCREEN_WIDTH // 2
        self.y = s.SCREEN_HEIGHT - s.PLAYER_Y_OFFSET
        self.width = s.PLAYER_WIDTH
        self.height = s.PLAYER_HEIGHT
        self.speed = s.PLAYER_SPEED
        self.invincible_timer = 0
        self._visible = True

        self.image = self._load_sprite()

        if self.image:
            self.shape_id = self.canvas.create_image(
                self.x, self.y, image=self.image, anchor="center"
            )
        else:
            hw = self.width // 2
            hh = self.height // 2
            self.shape_id = self.canvas.create_polygon(
                self.x, self.y - hh,
                self.x - hw, self.y + hh,
                self.x + hw, self.y + hh,
                fill="#00FF00", outline="#FFFFFF"
            )

    def _load_sprite(self):
        path = os.path.join(s.ASSETS_DIR, s.PLAYER_SPRITE)
        if os.path.exists(path):
            try:
                pil_img = Image.open(path).convert("RGBA")
                resized = pil_img.resize((self.width, self.height), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(resized)
            except Exception:
                pass
        return None

    def move(self, direction: int):
        dx = direction * self.speed
        new_x = self.x + dx
        half_w = self.width // 2

        if new_x - half_w < 10:
            new_x = half_w + 10
        elif new_x + half_w > s.SCREEN_WIDTH - 10:
            new_x = s.SCREEN_WIDTH - half_w - 10

        actual_dx = new_x - self.x
        self.x = new_x
        self.canvas.move(self.shape_id, actual_dx, 0)

    def get_nose_pos(self) -> tuple[int, int]:
        return (self.x, self.y - self.height // 2)

    def get_bbox(self) -> tuple[float, float, float, float]:
        half_w = self.width // 2
        half_h = self.height // 2
        return (self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h)

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            should_show = (self.invincible_timer % 8) < 4
            new_state = "normal" if should_show else "hidden"
            self.canvas.itemconfigure(self.shape_id, state=new_state)
            self._visible = should_show
        elif not self._visible:
            self.canvas.itemconfigure(self.shape_id, state="normal")
            self._visible = True

    @property
    def is_invincible(self) -> bool:
        return self.invincible_timer > 0

    def respawn(self):
        self.invincible_timer = getattr(s, "RESPAWN_DELAY_FRAMES", getattr(s, "RESPAWN_INVINCIBILITY", 120))
        old_x = self.x
        self.x = s.SCREEN_WIDTH // 2
        self.canvas.move(self.shape_id, self.x - old_x, 0)

    def destroy(self):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
            self.shape_id = None
