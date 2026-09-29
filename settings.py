import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

if not os.path.exists(ASSETS_DIR):
    ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_SPEED_MS = 16
WINDOW_TITLE = "Space Invaders — Basic Edition"

COLOR_BG = "#000000"
COLOR_PLAYER = "#00FF00"
COLOR_PLAYER_BULLET = "#00FFFF"
COLOR_ALIEN_BULLET = "#FF3333"
COLOR_TEXT = "#FFFFFF"
COLOR_STAR = "#444444"

PLAYER_SPEED = 6
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 42
PLAYER_SPRITE = "fighter_blue.png"
PLAYER_LIVES = 3
PLAYER_Y_OFFSET = 50
RESPAWN_DELAY_FRAMES = 120
RESPAWN_INVINCIBILITY = 120
MAX_PLAYER_BULLETS = 3
PLAYER_SHOOT_COOLDOWN = 15

BULLET_WIDTH = 4
BULLET_HEIGHT = 14
PLAYER_BULLET_SPEED = -8
ALIEN_BULLET_SPEED = 5

ALIEN_COLS = 8
ALIEN_ROWS = 5
ALIEN_WIDTH = 42
ALIEN_HEIGHT = 32
ALIEN_SPACING_X = 18
ALIEN_SPACING_Y = 14
ALIEN_START_X = 110
ALIEN_START_Y = 70
ALIEN_BASE_SPEED = 1.2
ALIEN_DROP_STEP = 20
ALIEN_SPEEDUP_PER_KILL = 0.08
ALIEN_SHOOT_CHANCE = 0.003

ALIEN_TYPES = [
    {"sprite": "ufo_purple.png",       "points": 30},
    {"sprite": "warship_red.png",      "points": 25},
    {"sprite": "claw_purple.png",      "points": 20},
    {"sprite": "interceptor_blue.png", "points": 15},
    {"sprite": "spider_red.png",       "points": 10},
]

FONT_FAMILY = "Courier"
FONT_SMALL = 14
FONT_MEDIUM = 24
FONT_LARGE = 44
