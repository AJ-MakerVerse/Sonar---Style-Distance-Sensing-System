import pygame
import math
import serial
import time

# ============================================================
# SERIAL CONFIGURATION (Arduino / Sensor Communication)
# ============================================================
PORT = "COM6"                 # Serial port Arduino is connected to
BAUD = 9600                   # Baud rate must match Arduino
TIMEOUT = 0.1                 # Serial read timeout
RECONNECT_INTERVAL = 2.0      # Seconds between reconnect attempts

# ============================================================
# DISPLAY / WINDOW CONFIGURATION
# ============================================================
WIDTH, HEIGHT = 1400, 700     # Window size
FPS = 60                      # Frames per second

SONAR_RADIUS = 460            # Radius of sonar arc
SONAR_CENTER = (WIDTH // 2, HEIGHT - 80)  # Bottom-center of screen

# ============================================================
# SONAR RANGE CONFIGURATION
# ============================================================
MAX_RANGE_CM = 50             # Max sensor distance
RING_STEP_CM = 10             # Distance between rings
RING_COUNT = MAX_RANGE_CM // RING_STEP_CM

SWEEP_WIDTH = 5               # Width of the sweep line
TRAIL_SPAN_DEG = 20           # Degrees of sweep trail

# ============================================================
# TARGET DOT CONFIGURATION
# ============================================================
DOT_RADIUS = 20               # Size of detected target dots

# ============================================================
# COLOR DEFINITIONS (RGB)
# ============================================================
BG = (0, 0, 0)                # Background
GREEN = (0, 220, 0)           # Main sonar green
GREEN_DIM = (0, 140, 0)       # Dimmed grid green
SWEEP = (0, 255, 120)         # Sweep beam color
RED = (255, 50, 50)           # Target color

# ============================================================
# PYGAME INITIALIZATION
# ============================================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SONAR")
clock = pygame.time.Clock()

# Surface used for fading sweep trail
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Fonts
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont("impact", 120)

# ============================================================
# SERIAL STATE VARIABLES
# ============================================================
arduino = None                # Serial object
last_serial_time = 0          # Last valid data time
last_reconnect = 0            # Last reconnect attempt time
SERIAL_TIMEOUT_UI = 1.0       # Time before "NO SIGNAL" shows

def try_reconnect_serial():
    """
    Attempt to reconnect to the serial port every RECONNECT_INTERVAL seconds.
    """
    global arduino, last_reconnect

    if time.time() - last_reconnect < RECONNECT_INTERVAL:
        return

    last_reconnect = time.time()

    try:
        arduino = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        arduino.flush()
    except:
        arduino = None

# ============================================================
# SONAR STATE VARIABLES
# ============================================================
current_angle = 0             # Current sweep angle
last_angle = 0                # Previous angle
direction = 1                # Sweep direction (left/right)
detections = {}               # Stored detections: angle → distance

# ============================================================
# DOT SIZE CONTROL (easy to expand later)
# ============================================================
def get_dot_radius():
    return DOT_RADIUS

# ============================================================
# MAIN APPLICATION LOOP
# ============================================================
running = True
while running:
    dt = clock.tick(FPS) / 1000
    now = time.time()

    # --------------------------------------------------------
    # HANDLE WINDOW EVENTS
    # --------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --------------------------------------------------------
    # SERIAL COMMUNICATION HANDLING
    # --------------------------------------------------------
    if arduino is None:
        try_reconnect_serial()

    if arduino and arduino.in_waiting:
        try:
            # Expected format: angle,distance
            line = arduino.readline().decode().strip()
            angle_str, dist_str = line.split(",")

            last_angle = current_angle
            current_angle = int(angle_str) - 90  # Center at 0°
            direction = 1 if current_angle > last_angle else -1
            last_serial_time = now

            # "-" means no detection at this angle
            if dist_str == "-":
                detections.pop(current_angle, None)
            else:
                detections[current_angle] = int(dist_str)

        except:
            arduino = None

    serial_active = (now - last_serial_time) < SERIAL_TIMEOUT_UI

    # --------------------------------------------------------
    # NO SIGNAL SCREEN
    # --------------------------------------------------------
    if not serial_active:
        screen.fill(BG)

        # Flashing warning text
        if int(now * 2) % 2 == 0:
            txt = big_font.render("NO SIGNAL DETECTED", True, RED)
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()
        continue

    # --------------------------------------------------------
    # CLEAR SCREEN & FADE TRAIL
    # --------------------------------------------------------
    screen.fill(BG)
    trail_surface.fill((0, 0, 0, 35), special_flags=pygame.BLEND_RGBA_MULT)

    # --------------------------------------------------------
    # RANGE ARCS (DISTANCE RINGS)
    # --------------------------------------------------------
    for i in range(1, RING_COUNT + 1):
        dist = i * RING_STEP_CM
        r = SONAR_RADIUS * dist / MAX_RANGE_CM
        rect = pygame.Rect(0, 0, r * 2, r * 2)
        rect.center = SONAR_CENTER

        pygame.draw.arc(
            screen,
            GREEN if dist == MAX_RANGE_CM else GREEN_DIM,
            rect,
            0,
            math.pi,
            4
        )

    # --------------------------------------------------------
    # BASELINE (GROUND LINE)
    # --------------------------------------------------------
    pygame.draw.line(
        screen,
        GREEN,
        (SONAR_CENTER[0] - SONAR_RADIUS, SONAR_CENTER[1]),
        (SONAR_CENTER[0] + SONAR_RADIUS, SONAR_CENTER[1]),
        5
    )

    # --------------------------------------------------------
    # DISTANCE TICKS AND LABELS
    # --------------------------------------------------------
    for i in range(RING_COUNT + 1):
        d = i * RING_STEP_CM
        r = SONAR_RADIUS * d / MAX_RANGE_CM

        for side in (-1, 1):
            x = SONAR_CENTER[0] + side * r
            pygame.draw.line(screen, GREEN, (x, SONAR_CENTER[1] - 14),
                             (x, SONAR_CENTER[1] + 14), 3)

            label = font.render(f"{d}cm", True, GREEN)
            screen.blit(label, label.get_rect(midtop=(x, SONAR_CENTER[1] + 18)))

    # --------------------------------------------------------
    # RADIAL GRID LINES (EVERY 30°)
    # --------------------------------------------------------
    for a in range(-90, 91, 30):
        rad = math.radians(a - 90)
        x = SONAR_CENTER[0] + SONAR_RADIUS * math.cos(rad)
        y = SONAR_CENTER[1] + SONAR_RADIUS * math.sin(rad)
        pygame.draw.line(screen, GREEN_DIM, SONAR_CENTER, (x, y), 3)

    # --------------------------------------------------------
    # ANGLE TICKS AND LABELS
    # --------------------------------------------------------
    for a in range(-90, 91, 5):
        rad = math.radians(a - 90)
        size = 18 if a % 10 == 0 else 10

        r1, r2 = SONAR_RADIUS - size, SONAR_RADIUS + size
        x1 = SONAR_CENTER[0] + r1 * math.cos(rad)
        y1 = SONAR_CENTER[1] + r1 * math.sin(rad)
        x2 = SONAR_CENTER[0] + r2 * math.cos(rad)
        y2 = SONAR_CENTER[1] + r2 * math.sin(rad)

        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2),
                         4 if a % 10 == 0 else 2)

        if a % 10 == 0:
            label = font.render(f"{abs(a)}°", True, GREEN)
            lx = SONAR_CENTER[0] + (SONAR_RADIUS + 45) * math.cos(rad)
            ly = SONAR_CENTER[1] + (SONAR_RADIUS + 45) * math.sin(rad)
            screen.blit(label, label.get_rect(center=(lx, ly)))

    # --------------------------------------------------------
    # SWEEP TRAIL (FADED AFTERIMAGE)
    # --------------------------------------------------------
    steps = 100
    for i in range(steps):
        offset = (i / steps) * TRAIL_SPAN_DEG
        a = current_angle - offset * direction

        if not -90 <= a <= 90:
            continue

        alpha = int(220 * (1 - i / steps))
        rad = math.radians(a - 90)

        x = SONAR_CENTER[0] + SONAR_RADIUS * math.cos(rad)
        y = SONAR_CENTER[1] + SONAR_RADIUS * math.sin(rad)

        pygame.draw.line(trail_surface, (0, 255, 120, alpha),
                         SONAR_CENTER, (x, y), 3)

    # --------------------------------------------------------
    # MAIN SWEEP LINE
    # --------------------------------------------------------
    rad = math.radians(current_angle - 90)
    sx = SONAR_CENTER[0] + SONAR_RADIUS * math.cos(rad)
    sy = SONAR_CENTER[1] + SONAR_RADIUS * math.sin(rad)
    pygame.draw.line(screen, SWEEP, SONAR_CENTER, (sx, sy), SWEEP_WIDTH)

    # --------------------------------------------------------
    # TARGET DOTS
    # --------------------------------------------------------
    for a, d in detections.items():
        if d > MAX_RANGE_CM:
            continue

        rad = math.radians(a - 90)
        r = SONAR_RADIUS * d / MAX_RANGE_CM

        x = SONAR_CENTER[0] + r * math.cos(rad)
        y = SONAR_CENTER[1] + r * math.sin(rad)

        pygame.draw.circle(screen, RED, (int(x), int(y)), get_dot_radius())

    # --------------------------------------------------------
    # FINAL DRAW
    # --------------------------------------------------------
    screen.blit(trail_surface, (0, 0))
    pygame.display.flip()

pygame.quit()
