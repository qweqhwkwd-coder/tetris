import pygame
import random
import sys

# simple_tetris.py
# A compact Tetris clone using pygame
# Save as main.py and run: python main.py
# Controls: ← → to move, ↑ to rotate, ↓ to soft drop, SPACE to hard drop, P to pause, ESC to quit


pygame.init()
pygame.display.set_caption("Tetris")

# Game constants
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
SIDE_PANEL = 200
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
COLORS = [
    (0, 240, 240),  # I - cyan
    (0, 0, 240),    # J - blue
    (240, 160, 0),  # L - orange
    (240, 240, 0),  # O - yellow
    (0, 240, 0),    # S - green
    (160, 0, 240),  # T - purple
    (240, 0, 0),    # Z - red
]

# Tetromino shapes (4x4 matrix strings)
SHAPES = [
    ["....",
     "IIII",
     "....",
     "...."],

    ["J..",
     "JJJ",
     "..."],

    ["..L",
     "LLL",
     "..."],

    ["OO",
     "OO"],

    [".SS",
     "SS.",
     "..."],

    [".T.",
     "TTT",
     "..."],

    ["ZZ.",
     ".ZZ",
     "..."],
]

# Normalize shapes: convert to list of rotation states of coordinates
def rotations_from_pattern(pattern):
    # pattern: list of strings (rows), variable size
    grid = [list(row) for row in pattern]
    size = len(grid)
    # pad to 4x4 for consistent rotations
    padded = [['.' for _ in range(4)] for _ in range(4)]
    for r in range(size):
        for c in range(len(grid[r])):
            padded[r][c] = grid[r][c]
    states = []
    mat = padded
    for _ in range(4):
        coords = []
        for r in range(4):
            for c in range(4):
                if mat[r][c] != '.':
                    coords.append((r, c))
        min_r = min([p[0] for p in coords])
        min_c = min([p[1] for p in coords])
        norm = sorted([(r - min_r, c - min_c) for r, c in coords])
        if norm not in states:
            states.append(norm)
        # rotate 90 degrees
        mat = [list(row) for row in zip(*mat[::-1])]
    return states

SHAPES_ROT = [rotations_from_pattern(p) for p in SHAPES]

class Piece:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.rot = 0
        self.states = SHAPES_ROT[shape_idx]
        self.color = COLORS[shape_idx]

    def get_cells(self, x_offset=0, y_offset=0, rot=None):
        if rot is None:
            rot = self.rot
        cells = []
        for r, c in self.states[rot]:
            cells.append((self.x + c + x_offset, self.y + r + y_offset))
        return cells

def create_grid(locked_positions=None):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    if locked_positions:
        for (x, y), color in locked_positions.items():
            if 0 <= y < ROWS and 0 <= x < COLS:
                grid[y][x] = color
    return grid

def valid_space(piece, locked):
    for x, y in piece.get_cells():
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and (x, y) in locked:
            return False
    return True

def check_lost(locked):
    for (x, y) in locked:
        if y < 1:
            return True
    return False

def get_random_piece():
    idx = random.randrange(len(SHAPES_ROT))
    # spawn near top center
    return Piece(COLS // 2 - 2, -1, idx)

def clear_rows(grid, locked):
    cleared = 0
    for r in range(ROWS - 1, -1, -1):
        if all(grid[r][c] != BLACK for c in range(COLS)):
            cleared += 1
            # remove locked blocks in that row
            for c in range(COLS):
                if (c, r) in locked:
                    del locked[(c, r)]
            # shift everything down
            for key in sorted(list(locked.keys()), key=lambda p: p[1])[::-1]:
                x, y = key
                if y < r:
                    color = locked.pop(key)
                    locked[(x, y + 1)] = color
    return cleared

def draw_text_middle(surface, text, size, color, offset_x=0, offset_y=0):
    font = pygame.font.SysFont('Calibri', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (WIDTH // 2 - label.get_width() // 2 + offset_x,
                         HEIGHT // 2 - label.get_height() // 2 + offset_y))

def draw_grid(surface, grid):
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(surface, grid[r][c],
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, GRAY,
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_side_panel(surface, score, level, next_piece):
    panel_x = WIDTH + 20
    font = pygame.font.SysFont('Calibri', 24)
    title = font.render("Next:", True, WHITE)
    surface.blit(title, (panel_x, 20))

    # Draw next piece in a small box
    box_x = panel_x
    box_y = 60
    box_size = CELL_SIZE
    for r in range(4):
        for c in range(4):
            pygame.draw.rect(surface, BLACK,
                             (box_x + c * box_size, box_y + r * box_size, box_size, box_size))
            pygame.draw.rect(surface, GRAY,
                             (box_x + c * box_size, box_y + r * box_size, box_size, box_size), 1)

    if next_piece:
        for x, y in next_piece.get_cells(x_offset=0, y_offset=0, rot=0):
            # next_piece coordinates are relative; shift to top-left of box
            nx = box_x + (x - next_piece.x + 1) * box_size
            ny = box_y + (y - next_piece.y + 1) * box_size
            pygame.draw.rect(surface, next_piece.color, (nx, ny, box_size, box_size))
            pygame.draw.rect(surface, GRAY, (nx, ny, box_size, box_size), 1)

    score_label = font.render(f"Score: {score}", True, WHITE)
    level_label = font.render(f"Level: {level}", True, WHITE)
    surface.blit(score_label, (panel_x, box_y + 5 * box_size))
    surface.blit(level_label, (panel_x, box_y + 5 * box_size + 30))

def draw_window(surface, grid, score, level, next_piece):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    # side panel background
    pygame.draw.rect(surface, (20, 20, 20), (WIDTH, 0, SIDE_PANEL, HEIGHT))
    draw_side_panel(surface, score, level, next_piece)
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIDTH + SIDE_PANEL, HEIGHT))
    clock = pygame.time.Clock()
    locked_positions = {}  # (x,y): color
    grid = create_grid(locked_positions)

    current_piece = get_random_piece()
    next_piece = get_random_piece()
    change_piece = False
    running = True
    paused = False
    fall_time = 0
    fall_speed = 0.8  # seconds per cell, decreases with level
    level = 1
    score = 0
    lines_cleared_total = 0

    while running:
        dt = clock.tick(FPS) / 1000.0
        if not paused:
            fall_time += dt

        # adjust speed by level
        fall_speed = max(0.05, 0.8 - (level - 1) * 0.07)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, locked_positions):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, locked_positions):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, locked_positions):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rot = (current_piece.rot + 1) % len(current_piece.states)
                        if not valid_space(current_piece, locked_positions):
                            # try wall kicks (simple)
                            kicked = False
                            for dx in (-1, 1, -2, 2):
                                current_piece.x += dx
                                if valid_space(current_piece, locked_positions):
                                    kicked = True
                                    break
                                current_piece.x -= dx
                            if not kicked:
                                current_piece.rot = (current_piece.rot - 1) % len(current_piece.states)
                    elif event.key == pygame.K_SPACE:
                        # hard drop
                        while valid_space(current_piece, locked_positions):
                            current_piece.y += 1
                        current_piece.y -= 1
                        change_piece = True

        if not paused and fall_time >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, locked_positions):
                current_piece.y -= 1
                change_piece = True

        # Lock piece and spawn next
        if change_piece:
            for x, y in current_piece.get_cells():
                if y < 0:
                    # piece is above top -> game over
                    running = False
                    break
                locked_positions[(x, y)] = current_piece.color
            current_piece = next_piece
            next_piece = get_random_piece()
            change_piece = False

            grid = create_grid(locked_positions)
            cleared = clear_rows(grid, locked_positions)
            if cleared > 0:
                lines_cleared_total += cleared
                # scoring: simple scheme
                score += {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared, cleared * 200)
                level = lines_cleared_total // 10 + 1
            grid = create_grid(locked_positions)

        # draw current piece onto a working grid copy
        temp_grid = create_grid(locked_positions)
        for x, y in current_piece.get_cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                temp_grid[y][x] = current_piece.color

        draw_window(win, temp_grid, score, level, next_piece)

    # Game over screen
    win.fill(BLACK)
    draw_text_middle(win, "GAME OVER", 48, WHITE)
    font = pygame.font.SysFont('Calibri', 24)
    label = font.render(f"Score: {score}", True, WHITE)
    win.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()