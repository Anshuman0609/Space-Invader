import settings as s

class Bullet:
    def __init__(self, canvas, x: float, y: float, speed: float, color: str):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.width = s.BULLET_WIDTH
        self.height = s.BULLET_HEIGHT

        half_w = self.width / 2
        half_h = self.height / 2
        self.shape_id = self.canvas.create_rectangle(
            x - half_w, y - half_h,
            x + half_w, y + half_h,
            fill=color,
            outline=""
        )

    def update(self) -> bool:
        self.y += self.speed
        self.canvas.move(self.shape_id, 0, self.speed)
        return -self.height <= self.y <= s.SCREEN_HEIGHT + self.height

    def get_bbox(self) -> tuple[float, float, float, float]:
        half_w = self.width / 2
        half_h = self.height / 2
        return (self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h)

    def destroy(self):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
            self.shape_id = None
