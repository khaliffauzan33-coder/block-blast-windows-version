import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# ==================================================
# WINDOW
# ==================================================

WIDTH = 600
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")

clock = pygame.time.Clock()

# ==================================================
# COLORS
# ==================================================

BG = (24, 24, 34)
GRID = (55, 55, 70)

WHITE = (245, 245, 245)
GRAY = (130, 130, 145)

RED = (235, 70, 70)
GREEN = (80, 220, 120)
BLUE = (70, 120, 230)
YELLOW = (255, 215, 70)

DARK = (15, 15, 23)

COLORS = [
    (70, 170, 255),
    (255, 90, 90),
    (90, 220, 120),
    (255, 200, 70),
    (180, 100, 255),
    (255, 140, 70)
]

# ==================================================
# FONT
# ==================================================

font_title = pygame.font.SysFont(
    "arial", 55, bold=True
)

font_big = pygame.font.SysFont(
    "arial", 40, bold=True
)

font = pygame.font.SysFont(
    "arial", 26, bold=True
)

font_small = pygame.font.SysFont(
    "arial", 19
)

# ==================================================
# BOARD
# ==================================================

ROWS = 8
COLS = 8
CELL = 55

BOARD_X = 80
BOARD_Y = 110

board = [
    [None for _ in range(COLS)]
    for _ in range(ROWS)
]

# ==================================================
# SHAPES
# ==================================================

SHAPES = [

    [(0, 0)],

    [(0, 0), (1, 0)],

    [(0, 0), (1, 0), (2, 0)],

    [(0, 0), (0, 1), (0, 2)],

    [
        (0, 0), (1, 0),
        (0, 1), (1, 1)
    ],

    [
        (0, 0), (1, 0), (2, 0),
        (1, 1)
    ],

    [
        (0, 0), (0, 1), (0, 2),
        (1, 2)
    ],

    [
        (0, 0), (1, 0),
        (1, 1), (2, 1)
    ],

    [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1)
    ],

    [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2)
    ],

    [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)
    ]
]

# ==================================================
# BLOCK
# ==================================================

def create_block():

    return {
        "shape": random.choice(SHAPES),
        "color": random.choice(COLORS),
        "used": False
    }


def create_blocks():

    return [
        create_block(),
        create_block(),
        create_block()
    ]


blocks = create_blocks()

# ==================================================
# SCORE
# ==================================================

score = 0

if os.path.exists("highscore.txt"):

    try:

        with open("highscore.txt", "r") as file:
            highscore = int(file.read())

    except:

        highscore = 0

else:

    highscore = 0


def save_highscore():

    with open("highscore.txt", "w") as file:
        file.write(str(highscore))

# ==================================================
# AUDIO CHECK
# ==================================================

music_volume = 0.5
sfx_volume = 0.7

music_ok = False
place_ok = False
clear_ok = False

place_sound = None
clear_sound = None

# --------------------------------------------------
# MUSIC
# --------------------------------------------------

if os.path.exists("music.mp3"):

    try:

        pygame.mixer.music.load("music.mp3")

        pygame.mixer.music.set_volume(
            music_volume
        )

        pygame.mixer.music.play(-1)

        music_ok = True

        print("MUSIC: ON")
        print("music.mp3 ditemukan dan berhasil dimainkan.")

    except Exception as e:

        print("MUSIC: OFF")
        print("Error:", e)

else:

    print("MUSIC: OFF")
    print("music.mp3 tidak ditemukan.")

# --------------------------------------------------
# PLACE SOUND
# --------------------------------------------------

if os.path.exists("place.wav"):

    try:

        place_sound = pygame.mixer.Sound(
            "place.wav"
        )

        place_sound.set_volume(
            sfx_volume
        )

        place_ok = True

        print("PLACE SFX: ON")

    except Exception as e:

        print("PLACE SFX: OFF")
        print("Error:", e)

else:

    print("PLACE SFX: OFF")

# --------------------------------------------------
# CLEAR SOUND
# --------------------------------------------------

if os.path.exists("clear.wav"):

    try:

        clear_sound = pygame.mixer.Sound(
            "clear.wav"
        )

        clear_sound.set_volume(
            sfx_volume
        )

        clear_ok = True

        print("CLEAR SFX: ON")

    except Exception as e:

        print("CLEAR SFX: OFF")
        print("Error:", e)

else:

    print("CLEAR SFX: OFF")


# ==================================================
# PLAY SOUND
# ==================================================

def play_place_sound():

    if place_sound and place_ok:

        place_sound.set_volume(
            sfx_volume
        )

        place_sound.play()


def play_clear_sound():

    if clear_sound and clear_ok:

        clear_sound.set_volume(
            sfx_volume
        )

        clear_sound.play()


# ==================================================
# GAME STATES
# ==================================================

HOME = "home"
GAME = "game"
MENU = "menu"
SETTINGS = "settings"
GAME_OVER = "gameover"

state = HOME

# ==================================================
# DRAG
# ==================================================

dragging = None

mouse_x = 0
mouse_y = 0

BLOCK_POSITIONS = [
    (70, 610),
    (270, 610),
    (470, 610)
]

# ==================================================
# RESET
# ==================================================

def reset_game():

    global board
    global blocks
    global score
    global dragging

    board = [
        [None for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    blocks = create_blocks()

    score = 0

    dragging = None

# ==================================================
# BUTTON
# ==================================================

def draw_button(text, rect, color):

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=14
    )

    surface = font.render(
        text,
        True,
        WHITE
    )

    screen.blit(
        surface,
        (
            rect.centerx -
            surface.get_width() // 2,

            rect.centery -
            surface.get_height() // 2
        )
    )

# ==================================================
# PLACE CHECK
# ==================================================

def can_place(block, row, col):

    for dx, dy in block["shape"]:

        r = row + dy
        c = col + dx

        if r < 0 or r >= ROWS:
            return False

        if c < 0 or c >= COLS:
            return False

        if board[r][c] is not None:
            return False

    return True


def place_block(block, row, col):

    for dx, dy in block["shape"]:

        board[row + dy][col + dx] = \
            block["color"]

# ==================================================
# FIND LINES
# ==================================================

def find_lines():

    rows = []
    cols = []

    for r in range(ROWS):

        if all(
            board[r][c] is not None
            for c in range(COLS)
        ):

            rows.append(r)

    for c in range(COLS):

        if all(
            board[r][c] is not None
            for r in range(ROWS)
        ):

            cols.append(c)

    return rows, cols

# ==================================================
# CLEAR ANIMATION
# ==================================================

def clear_animation(rows, cols):

    global score

    particles = []

    for r in rows:

        for c in range(COLS):

            color = board[r][c]

            if color:

                x = (
                    BOARD_X +
                    c * CELL +
                    CELL // 2
                )

                y = (
                    BOARD_Y +
                    r * CELL +
                    CELL // 2
                )

                for _ in range(5):

                    particles.append({

                        "x": x,
                        "y": y,

                        "vx": random.uniform(
                            -4, 4
                        ),

                        "vy": random.uniform(
                            -5, 1
                        ),

                        "life": random.randint(
                            15, 30
                        ),

                        "color": color
                    })

    for c in cols:

        for r in range(ROWS):

            if r in rows:
                continue

            color = board[r][c]

            if color:

                x = (
                    BOARD_X +
                    c * CELL +
                    CELL // 2
                )

                y = (
                    BOARD_Y +
                    r * CELL +
                    CELL // 2
                )

                for _ in range(5):

                    particles.append({

                        "x": x,
                        "y": y,

                        "vx": random.uniform(
                            -4, 4
                        ),

                        "vy": random.uniform(
                            -5, 1
                        ),

                        "life": random.randint(
                            15, 30
                        ),

                        "color": color
                    })

    play_clear_sound()

    for frame in range(25):

        screen.fill(BG)

        draw_game()

        if frame < 8:

            flash = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            alpha = max(
                0,
                130 - frame * 16
            )

            flash.fill(
                (255, 255, 255, alpha)
            )

            screen.blit(
                flash,
                (0, 0)
            )

        for particle in particles:

            pygame.draw.circle(
                screen,
                particle["color"],
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                4
            )

            particle["x"] += \
                particle["vx"]

            particle["y"] += \
                particle["vy"]

            particle["vy"] += 0.25

            particle["life"] -= 1

        particles[:] = [
            p for p in particles
            if p["life"] > 0
        ]

        pygame.display.flip()

        clock.tick(60)

    for r in rows:

        for c in range(COLS):

            board[r][c] = None

    for c in cols:

        for r in range(ROWS):

            board[r][c] = None

    total = len(rows) + len(cols)

    score += total * 10

    if total >= 2:

        score += total * 15

# ==================================================
# GAME OVER CHECK
# ==================================================

def check_game_over():

    for block in blocks:

        if block["used"]:
            continue

        for r in range(ROWS):

            for c in range(COLS):

                if can_place(
                    block,
                    r,
                    c
                ):

                    return False

    return True

# ==================================================
# DRAW BOARD
# ==================================================

def draw_board():

    for r in range(ROWS):

        for c in range(COLS):

            x = BOARD_X + c * CELL
            y = BOARD_Y + r * CELL

            pygame.draw.rect(
                screen,
                GRID,
                (
                    x + 2,
                    y + 2,
                    CELL - 4,
                    CELL - 4
                ),
                border_radius=7
            )

            if board[r][c]:

                pygame.draw.rect(
                    screen,
                    board[r][c],
                    (
                        x + 5,
                        y + 5,
                        CELL - 10,
                        CELL - 10
                    ),
                    border_radius=7
                )

# ==================================================
# HEADER
# ==================================================

def draw_header():

    title = font_big.render(
        "BLOCK BLAST",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            25
        )
    )

    score_text = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 70)
    )

    high_text = font.render(
        "High: " + str(highscore),
        True,
        YELLOW
    )

    screen.blit(
        high_text,
        (410, 70)
    )

# ==================================================
# DRAW BLOCKS
# ==================================================

def draw_blocks():

    for i in range(3):

        block = blocks[i]

        if block["used"]:
            continue

        x, y = BLOCK_POSITIONS[i]

        for dx, dy in block["shape"]:

            pygame.draw.rect(
                screen,
                block["color"],
                (
                    x + dx * 30,
                    y + dy * 30,
                    27,
                    27
                ),
                border_radius=5
            )

# ==================================================
# FIND BLOCK
# ==================================================

def find_block(mx, my):

    for i in range(3):

        block = blocks[i]

        if block["used"]:
            continue

        x, y = BLOCK_POSITIONS[i]

        max_x = max(
            dx for dx, dy
            in block["shape"]
        )

        max_y = max(
            dy for dx, dy
            in block["shape"]
        )

        rect = pygame.Rect(
            x - 15,
            y - 15,
            (max_x + 1) * 30 + 30,
            (max_y + 1) * 30 + 30
        )

        if rect.collidepoint(mx, my):

            return i

    return None

# ==================================================
# DRAG DRAW
# ==================================================

def draw_drag():

    if dragging is None:
        return

    block = blocks[dragging]

    target_y = mouse_y - 50

    col = int(
        (mouse_x - BOARD_X) /
        CELL
    )

    row = int(
        (target_y - BOARD_Y) /
        CELL
    )

    if (
        0 <= row < ROWS
        and 0 <= col < COLS
    ):

        valid = can_place(
            block,
            row,
            col
        )

        color = (
            block["color"]
            if valid
            else RED
        )

        for dx, dy in block["shape"]:

            r = row + dy
            c = col + dx

            if (
                0 <= r < ROWS
                and 0 <= c < COLS
            ):

                x = BOARD_X + c * CELL
                y = BOARD_Y + r * CELL

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        x + 7,
                        y + 7,
                        CELL - 14,
                        CELL - 14
                    ),
                    border_radius=6
                )

    for dx, dy in block["shape"]:

        pygame.draw.rect(
            screen,
            block["color"],
            (
                mouse_x - 20 + dx * 32,
                mouse_y - 70 + dy * 32,
                29,
                29
            ),
            border_radius=5
        )

# ==================================================
# DRAW GAME
# ==================================================

def draw_game():

    screen.fill(BG)

    draw_header()

    draw_board()

    draw_blocks()

    if dragging is not None:

        draw_drag()

# ==================================================
# HOME
# ==================================================

def draw_home():

    screen.fill(BG)

    title = font_title.render(
        "BLOCK BLAST",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            100
        )
    )

    subtitle = font_small.render(
        "Classic Block Puzzle",
        True,
        GRAY
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2 -
            subtitle.get_width() // 2,
            170
        )
    )

    play_button = pygame.Rect(
        170,
        245,
        260,
        65
    )

    menu_button = pygame.Rect(
        170,
        330,
        260,
        65
    )

    draw_button(
        "PLAY",
        play_button,
        GREEN
    )

    draw_button(
        "MENU",
        menu_button,
        BLUE
    )

    # ----------------------------------------------
    # AUDIO STATUS
    # ----------------------------------------------

    music_color = (
        GREEN if music_ok
        else RED
    )

    sfx_color = (
        GREEN if (place_ok or clear_ok)
        else RED
    )

    music_status = font_small.render(
        "MUSIC: " +
        ("ON" if music_ok else "OFF"),
        True,
        music_color
    )

    sfx_status = font_small.render(
        "SFX: " +
        ("ON" if (place_ok or clear_ok) else "OFF"),
        True,
        sfx_color
    )

    screen.blit(
        music_status,
        (
            170,
            440
        )
    )

    screen.blit(
        sfx_status,
        (
            350,
            440
        )
    )

    high_text = font.render(
        "High Score: " +
        str(highscore),
        True,
        YELLOW
    )

    screen.blit(
        high_text,
        (
            WIDTH // 2 -
            high_text.get_width() // 2,
            500
        )
    )

    return play_button, menu_button

# ==================================================
# SLIDER
# ==================================================

def draw_slider(
    name,
    value,
    y
):

    text = font.render(
        name,
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            100,
            y - 45
        )
    )

    slider = pygame.Rect(
        100,
        y,
        400,
        10
    )

    pygame.draw.rect(
        screen,
        GRID,
        slider,
        border_radius=5
    )

    filled = pygame.Rect(
        100,
        y,
        int(400 * value),
        10
    )

    pygame.draw.rect(
        screen,
        BLUE,
        filled,
        border_radius=5
    )

    knob_x = (
        100 +
        int(400 * value)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            knob_x,
            y + 5
        ),
        10
    )

    percent = font_small.render(
        str(int(value * 100)) + "%",
        True,
        WHITE
    )

    screen.blit(
        percent,
        (
            510,
            y - 5
        )
    )

# ==================================================
# SETTINGS
# ==================================================

def draw_settings():

    screen.fill(BG)

    title = font_big.render(
        "MENU",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            60
        )
    )

    high_text = font.render(
        "HIGH SCORE: " +
        str(highscore),
        True,
        YELLOW
    )

    screen.blit(
        high_text,
        (
            WIDTH // 2 -
            high_text.get_width() // 2,
            130
        )
    )

    draw_slider(
        "Music Volume",
        music_volume,
        250
    )

    draw_slider(
        "Sound Effects",
        sfx_volume,
        360
    )

    # Audio status
    music_status = font_small.render(
        "MUSIC: " +
        ("ON" if music_ok else "OFF"),
        True,
        GREEN if music_ok else RED
    )

    sfx_status = font_small.render(
        "SFX: " +
        ("ON" if (place_ok or clear_ok)
         else "OFF"),
        True,
        GREEN if (place_ok or clear_ok)
        else RED
    )

    screen.blit(
        music_status,
        (100, 425)
    )

    screen.blit(
        sfx_status,
        (350, 425)
    )

    back_button = pygame.Rect(
        170,
        510,
        260,
        65
    )

    draw_button(
        "BACK",
        back_button,
        RED
    )

    return back_button

# ==================================================
# IN-GAME MENU
# ==================================================

def draw_game_menu():

    draw_game()

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 180)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title = font_big.render(
        "MENU",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            180
        )
    )

    restart_button = pygame.Rect(
        170,
        280,
        260,
        65
    )

    home_button = pygame.Rect(
        170,
        370,
        260,
        65
    )

    draw_button(
        "RESTART",
        restart_button,
        BLUE
    )

    draw_button(
        "HOME",
        home_button,
        RED
    )

    return restart_button, home_button

# ==================================================
# GAME OVER
# ==================================================

def draw_game_over():

    draw_game()

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 190)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title = font_big.render(
        "GAME OVER",
        True,
        RED
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            210
        )
    )

    score_text = font.render(
        "Score: " +
        str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 -
            score_text.get_width() // 2,
            275
        )
    )

    restart_button = pygame.Rect(
        170,
        350,
        260,
        65
    )

    home_button = pygame.Rect(
        170,
        440,
        260,
        65
    )

    draw_button(
        "RESTART",
        restart_button,
        BLUE
    )

    draw_button(
        "HOME",
        home_button,
        RED
    )

    return restart_button, home_button

# ==================================================
# MAIN LOOP
# ==================================================

running = True

while running:

    # ==================================================
    # DRAW STATE
    # ==================================================

    if state == HOME:

        play_button, menu_button = \
            draw_home()

    elif state == GAME:

        draw_game()

        game_menu_button = pygame.Rect(
            470,
            20,
            105,
            45
        )

        draw_button(
            "MENU",
            game_menu_button,
            BLUE
        )

    elif state == SETTINGS:

        back_button = draw_settings()

    elif state == MENU:

        restart_button, home_button = \
            draw_game_menu()

    elif state == GAME_OVER:

        restart_button, home_button = \
            draw_game_over()

    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ==================================================
        # HOME
        # ==================================================

        elif state == HOME:

            if (
                event.type ==
                pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mx, my = pygame.mouse.get_pos()

                if play_button.collidepoint(
                    mx,
                    my
                ):

                    reset_game()

                    state = GAME

                elif menu_button.collidepoint(
                    mx,
                    my
                ):

                    state = SETTINGS

        # ==================================================
        # SETTINGS
        # ==================================================

        elif state == SETTINGS:

            if (
                event.type ==
                pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mx, my = pygame.mouse.get_pos()

                # BACK
                if back_button.collidepoint(
                    mx,
                    my
                ):

                    state = HOME

                # MUSIC SLIDER
                elif (
                    100 <= mx <= 500
                    and 235 <= my <= 275
                ):

                    music_volume = (
                        mx - 100
                    ) / 400

                    music_volume = max(
                        0,
                        min(1, music_volume)
                    )

                    pygame.mixer.music.set_volume(
                        music_volume
                    )

                # SFX SLIDER
                elif (
                    100 <= mx <= 500
                    and 345 <= my <= 385
                ):

                    sfx_volume = (
                        mx - 100
                    ) / 400

                    sfx_volume = max(
                        0,
                        min(1, sfx_volume)
                    )

                    if place_sound:

                        place_sound.set_volume(
                            sfx_volume
                        )

                    if clear_sound:

                        clear_sound.set_volume(
                            sfx_volume
                        )

        # ==================================================
        # GAME
        # ==================================================

        elif state == GAME:

            if (
                event.type ==
                pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mx, my = pygame.mouse.get_pos()

                if game_menu_button.collidepoint(
                    mx,
                    my
                ):

                    dragging = None

                    state = MENU

                else:

                    dragging = find_block(
                        mx,
                        my
                    )

                    mouse_x = mx
                    mouse_y = my

            elif event.type == pygame.MOUSEMOTION:

                if dragging is not None:

                    mouse_x, mouse_y = \
                        pygame.mouse.get_pos()

            elif (
                event.type ==
                pygame.MOUSEBUTTONUP
                and event.button == 1
            ):

                if dragging is not None:

                    mx, my = pygame.mouse.get_pos()

                    block = blocks[dragging]

                    target_y = my - 50

                    col = int(
                        (mx - BOARD_X) /
                        CELL
                    )

                    row = int(
                        (target_y - BOARD_Y) /
                        CELL
                    )

                    if can_place(
                        block,
                        row,
                        col
                    ):

                        place_block(
                            block,
                            row,
                            col
                        )

                        play_place_sound()

                        score += len(
                            block["shape"]
                        )

                        block["used"] = True

                        rows, cols = \
                            find_lines()

                        if rows or cols:

                            clear_animation(
                                rows,
                                cols
                            )

                        if score > highscore:

                            highscore = score

                            save_highscore()

                        if all(
                            b["used"]
                            for b in blocks
                        ):

                            blocks = \
                                create_blocks()

                        if check_game_over():

                            state = GAME_OVER

                    dragging = None

        # ==================================================
        # IN-GAME MENU
        # ==================================================

        elif state == MENU:

            if (
                event.type ==
                pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mx, my = pygame.mouse.get_pos()

                if restart_button.collidepoint(
                    mx,
                    my
                ):

                    reset_game()

                    state = GAME

                elif home_button.collidepoint(
                    mx,
                    my
                ):

                    dragging = None

                    state = HOME

        # ==================================================
        # GAME OVER
        # ==================================================

        elif state == GAME_OVER:

            if (
                event.type ==
                pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mx, my = pygame.mouse.get_pos()

                if restart_button.collidepoint(
                    mx,
                    my
                ):

                    reset_game()

                    state = GAME

                elif home_button.collidepoint(
                    mx,
                    my
                ):

                    state = HOME

    pygame.display.flip()

    clock.tick(60)

pygame.quit()