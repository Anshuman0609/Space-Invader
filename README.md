# Space Invaders — College Project (Basic Edition with Custom Sprites)

A 2D arcade Space Invaders game developed in Python using the built-in **Tkinter** graphical user interface library and **custom transparent spaceship sprites**. This edition is designed specifically as a college project submission: simple, modular, strictly **5 Python files**, and completely free of external dependencies beyond Pillow for image loading.

---

## 1. Project Overview

- **Project Title**: Space Invaders 2D Arcade Game
- **Language**: Python 3.x
- **GUI Framework**: Tkinter (`tkinter.Canvas`)
- **Graphics**: Custom transparent PNG spaceship sprites rendered with `ImageTk.PhotoImage`
- **Architecture**: Modular Object-Oriented Programming (OOP)
- **Total Code Files**: Exactly 5 Python source files

---

## 2. File Structure (Max 5 Python Files)

```
basic_version/
├── settings.py   # 1. Screen dimensions, speeds, asset paths, points, and constants
├── player.py     # 2. Player spaceship sprite class (Movement, bounds check, respawn)
├── bullet.py     # 3. Laser projectile class (Upward player & downward alien shots)
├── alien.py      # 4. Alien sprite class & 8x5 AlienGrid fleet formation manager
├── main.py       # 5. Game controller, 60 FPS loop, collision detection, Tk window
├── assets/       # Folder containing the 20 transparent spaceship PNG sprites
└── README.md     # Project documentation & viva defense guide
```

---

## 3. How to Run

Open your terminal or command prompt, navigate to the `basic_version` directory, and run:

```bash
cd basic_version
python main.py
```

---

## 4. Controls

| Key | Action |
|:---:|:---|
| `←` Left Arrow | Move spaceship to the left |
| `→` Right Arrow | Move spaceship to the right |
| `SPACE` | Fire laser cannon (up to 3 simultaneous bullets) |
| `ENTER` | Start game / Restart after Game Over |
| `ESC` | Exit game cleanly |

---

## 5. Scoring & Alien Ranks

The invasion fleet consists of 40 aliens arranged in an **8-column × 5-row** formation:

| Row | Sprite Asset | Class | Points | Description |
|:---:|:---:|:---:|:---:|:---|
| **Row 0 (Top)** | `ufo_purple.png` | Command Saucer | **30 PTS** | High-value command scout |
| **Row 1** | `warship_red.png` | Heavy Warship | **25 PTS** | Armored heavy assault ship |
| **Row 2** | `claw_purple.png` | Assault Claw | **20 PTS** | Mid-tier pincer striker |
| **Row 3** | `interceptor_blue.png` | Winged Scout | **15 PTS** | High-speed interceptor |
| **Row 4 (Front)** | `spider_red.png` | Spider Mech | **10 PTS** | Front-line mechanized swarm |

---

## 6. Technical Implementation Details (Viva / Presentation Guide)

### A. Rendering Image Sprites on Tkinter Canvas
Images with transparency are opened and resized with Pillow's `Image.Resampling.LANCZOS`, then converted to `ImageTk.PhotoImage`:
```python
pil_img = Image.open(path).convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
self.image = ImageTk.PhotoImage(pil_img)
self.shape_id = self.canvas.create_image(x, y, image=self.image, anchor="center")
```
*Key Viva Note*: A reference to the `PhotoImage` must be preserved in Python (e.g. `self.image`) to prevent Python's garbage collector from deleting the image from memory, which would cause canvas flickering.

### B. Non-Blocking Game Loop (`canvas.after`)
Arcade games require a continuous frame loop (~60 frames per second). In Tkinter, calling `time.sleep()` would freeze the GUI event loop. Instead, we use Tkinter's non-blocking timer:
```python
self.canvas.after(16, self._game_loop)
```
- `16 ms` delay corresponds to $\frac{1000 \text{ ms}}{60 \text{ FPS}} \approx 16.6 \text{ ms}$ per frame.

### C. Axis-Aligned Bounding Box (AABB) Collision Detection
Collisions are evaluated mathematically using AABB overlap:
```python
def check_overlap(box_a, box_b):
    return (box_a[0] < box_b[2] and   # a.left   < b.right
            box_a[2] > box_b[0] and   # a.right  > b.left
            box_a[1] < box_b[3] and   # a.top    < b.bottom
            box_a[3] > box_b[1])      # a.bottom > b.top
```

### D. Alien Fleet Formation AI
1. **Synchronized March**: The fleet moves together horizontally (`dx = speed * direction`).
2. **Edge Reversal & Step Down**: When any alien touches the left or right margin, the fleet reverses direction and drops down 20 pixels.
3. **Dynamic Acceleration**: As aliens are shot down, the fleet's speed progressively increases.
4. **Column Shooting**: Only the bottom-most alien in each active column is eligible to fire bullets downward.
