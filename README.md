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


## 2. How to Run

Open your terminal or command prompt, navigate to the `basic_version` directory, and run:

```bash
cd basic_version
python main.py
```

---

## 3. Controls

| Key | Action |
|:---:|:---|
| `←` Left Arrow | Move spaceship to the left |
| `→` Right Arrow | Move spaceship to the right |
| `SPACE` | Fire laser cannon (up to 3 simultaneous bullets) |
| `ENTER` | Start game / Restart after Game Over |
| `ESC` | Exit game cleanly |

---

## 4. Scoring & Alien Ranks

The invasion fleet consists of 40 aliens arranged in an **8-column × 5-row** formation:

| Row | Sprite Asset | Class | Points | Description |
|:---:|:---:|:---:|:---:|:---|
| **Row 0 (Top)** | `ufo_purple.png` | Command Saucer | **30 PTS** | High-value command scout |
| **Row 1** | `warship_red.png` | Heavy Warship | **25 PTS** | Armored heavy assault ship |
| **Row 2** | `claw_purple.png` | Assault Claw | **20 PTS** | Mid-tier pincer striker |
| **Row 3** | `interceptor_blue.png` | Winged Scout | **15 PTS** | High-speed interceptor |
| **Row 4 (Front)** | `spider_red.png` | Spider Mech | **10 PTS** | Front-line mechanized swarm |

---
