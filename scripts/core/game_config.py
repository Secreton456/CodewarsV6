# scripts/core/game_config.py

# =========================
# ENGINE / RUNTIME
# =========================
FPS = 60
FIXED_TIMESTEP = True
TIME_SCALE = 1.0
DEBUG = True


# =========================
# DEBUG / DEVELOPER TOOLS
# =========================
SHOW_FPS = True
SHOW_HITBOXES = False
SHOW_COLLISION_BOXES = False
SHOW_VELOCITY_VECTORS = False
LOG_EVENTS = True

GOD_MODE = False
INFINITE_AMMO = False
NO_RELOAD = False
FREE_CAMERA = False


# =========================
# WORLD / MAP
# =========================
TILE_SIZE = 32
MAP_WIDTH = 80
MAP_HEIGHT = 50

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

WORLD_BOUNDS = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Example spawn points (can be overridden per-map)
SPAWN_POINTS = [
    (100, 100),
    (SCREEN_WIDTH - 100, 100),
    (100, SCREEN_HEIGHT - 100),
    (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100),
]


# =========================
# CAMERA SYSTEM
# =========================
CAMERA_LERP = 0.1
CAMERA_ZOOM = 1.0
CAMERA_SHAKE_STRENGTH = 5
CAMERA_SHAKE_DURATION = 0.3
CAMERA_CLAMP_TO_MAP = True


# =========================
# PHYSICS RULES (GLOBAL)
# =========================
GRAVITY = 0.5
MAX_FALL_SPEED = 12
TERMINAL_VELOCITY = 20

GROUND_FRICTION = 0.9
AIR_RESISTANCE = 0.98

COLLISION_EPSILON = 0.01


# =========================
# PLAYER MOVEMENT RULES
# =========================
WALK_SPEED = 4
RUN_SPEED = 6
CROUCH_SPEED = 2
PRONE_SPEED = 1

MAX_VELOCITY = 15
JUMP_POWER = -10  # Negative because Y goes down

AIR_CONTROL = 0.6
KNOCKBACK_RESISTANCE = 0.2


# =========================
# JETPACK / THRUST SYSTEM
# =========================
THRUST_POWER = 0.8

MAX_FUEL = 100
FUEL_REGEN = 1
FUEL_USAGE_FLY = 2
FUEL_USAGE_BOOST = 3

JETPACK_COOLDOWN = 0.5  # seconds


# =========================
# PLAYER STATS
# =========================
MAX_HP = 100

PLAYER_WIDTH = 24
PLAYER_HEIGHT = 32
PLAYER_HITBOX_RADIUS = 12

INVULNERABILITY_TIME = 1  # seconds after respawn


# =========================
# WEAPONS — GLOBAL RULES
# =========================
DEFAULT_WEAPON = "pistol"

WEAPON_SWITCH_TIME = 0.5
RELOAD_ANIMATION_TIME = 1.5

DROP_WEAPON_ON_DEATH = True
MAX_WEAPONS_HELD = 2


# =========================
# WEAPONS — PER-WEAPON DATA
# =========================
WEAPONS = {
    "pistol": {
        "damage": 20,
        "fire_rate": 0.3,
        "ammo": 12,
        "reload_time": 1.5,
        "range": 500,
        "spread": 2,
        "recoil": 1,
        "bullet_speed": 25,
        "knockback": 2,
    },
    "smg": {
        "damage": 15,
        "fire_rate": 0.1,
        "ammo": 30,
        "reload_time": 2.0,
        "range": 400,
        "spread": 5,
        "recoil": 2,
        "bullet_speed": 28,
        "knockback": 2,
    },
    "sniper": {
        "damage": 80,
        "fire_rate": 1.5,
        "ammo": 5,
        "reload_time": 3.0,
        "range": 1000,
        "spread": 0,
        "recoil": 6,
        "bullet_speed": 45,
        "knockback": 6,
    },
    "shotgun": {
        "damage": 60,
        "fire_rate": 0.8,
        "ammo": 6,
        "reload_time": 2.5,
        "range": 200,
        "spread": 12,
        "recoil": 5,
        "bullet_speed": 22,
        "knockback": 5,
    },
    "rocket": {
        "damage": 100,
        "fire_rate": 2.0,
        "ammo": 3,
        "reload_time": 4.0,
        "range": 800,
        "spread": 0,
        "recoil": 8,
        "bullet_speed": 18,
        "knockback": 10,
        "splash_radius": 80,
    },
}


# =========================
# PROJECTILES / BULLETS
# =========================
BULLET_LIFETIME = 2.5  # seconds
BULLET_RADIUS = 3
BULLET_GRAVITY = 0.0
MAX_ACTIVE_BULLETS = 500


# =========================
# COMBAT RULES
# =========================
HEADSHOT_MULTIPLIER = 2.0
CRITICAL_HIT_CHANCE = 0.05

KNOCKBACK_FORCE = 5

FRIENDLY_FIRE = False
DAMAGE_FALLOFF = True


# =========================
# MELEE COMBAT
# =========================
MELEE_RANGE = 40
MELEE_DAMAGE = 50
MELEE_COOLDOWN = 0.5


# =========================
# HEALTH / DEATH / RESPAWN
# =========================
RESPAWN_TIME = 3

DROP_WEAPONS_ON_DEATH = True

HEALTH_REGEN = 0
HEALTH_REGEN_DELAY = 5  # seconds after taking damage


# =========================
# TEAMS / MULTIPLAYER
# =========================
MAX_TEAMS = 5
MAX_TROOPS_PER_TEAM = 10

TEAM_COLORS = [
    (255, 50, 50),    # Red
    (50, 100, 255),   # Blue
    (50, 255, 50),    # Green
    (255, 200, 50),   # Yellow
    (200, 50, 255),   # Purple
]

TEAM_DAMAGE_MULTIPLIER = 1.0
ALLOW_TEAM_SWITCHING = True


# =========================
# MATCH RULES
# =========================
MATCH_TIME_LIMIT = 300  # seconds
KILL_LIMIT = 50
SUDDEN_DEATH_TIME = 30

RESPAWN_ENABLED = True
SCORE_LIMIT = 100


# =========================
# AI / BOTS
# =========================
BOT_COUNT = 10
BOT_DIFFICULTY = 1.0  # 0.5 easy, 1.0 normal, 2.0 hard

BOT_REACTION_TIME = 0.3
BOT_ACCURACY = 0.6
BOT_AGGRESSION = 0.7


# =========================
# INPUT MAPPING (LOGICAL)
# =========================
MOVE_LEFT = "move_left"
MOVE_RIGHT = "move_right"
JUMP = "jump"
THRUST = "thrust"

SHOOT = "shoot"
RELOAD = "reload"
MELEE = "melee"
SWITCH_WEAPON = "switch_weapon"


# =========================
# VISUAL / FX TOGGLES
# =========================
ENABLE_PARTICLES = True
ENABLE_SCREEN_SHAKE = True
SHOW_DAMAGE_NUMBERS = True
ENABLE_MUZZLE_FLASH = True


# =========================
# PATHS / STRUCTURE
# =========================
ASSETS_DIR = "assets/"
SCRIPTS_DIR = "scripts/"
MAPS_DIR = "maps/"
SOUNDS_DIR = "sounds/"
SAVE_DIR = "saves/"

