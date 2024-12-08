import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Maze settings
cols, rows = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
maze = [[1 for _ in range(cols)] for _ in range(rows)]
visited = [[False for _ in range(cols)] for _ in range(rows)]
stack = []

# Player settings
player_x, player_y = 0, 0
player_rect = pygame.Rect(player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
player_speed = GRID_SIZE  # Move one grid cell per step

# Goal settings
goal_x, goal_y = cols - 1, rows - 1

# Movement controls
current_direction = None

# Movement directions
directions = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}


def create_maze(x, y):
    """Generate a random maze using recursive backtracking."""
    visited[y][x] = True
    stack.append((x, y))

    while stack:
        current_x, current_y = stack[-1]
        stack.pop()
        neighbors = []

        for dx, dy in directions.values():
            nx, ny = current_x + dx * 2, current_y + dy * 2
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                neighbors.append((nx, ny))

        if neighbors:
            stack.append((current_x, current_y))
            nx, ny = random.choice(neighbors)
            maze[current_y + (ny - current_y) // 2][current_x + (nx - current_x) // 2] = 0
            maze[ny][nx] = 0
            visited[ny][nx] = True
            stack.append((nx, ny))


def draw_maze():
    """Draw the maze."""
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def is_valid_move(grid_x, grid_y):
    """Check if a move is valid (within bounds and not a wall)."""
    if 0 <= grid_x < cols and 0 <= grid_y < rows and maze[grid_y][grid_x] == 0:
        return True
    return False


# Generate the maze
create_maze(0, 0)

# Ensure the goal is on a valid path
while maze[goal_y][goal_x] == 1:
    goal_x, goal_y = random.randint(0, cols - 1), random.randint(0, rows - 1)

# Enable key repeat for smooth movement
pygame.key.set_repeat(100, 100)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_maze()

    # Draw the player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw the goal
    pygame.draw.rect(screen, RED, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses for movement
        elif event.type == pygame.KEYDOWN:
            if event.key in directions:
                dx, dy = directions[event.key]
                grid_x = player_rect.x // GRID_SIZE + dx
                grid_y = player_rect.y // GRID_SIZE + dy

                if is_valid_move(grid_x, grid_y):
                    player_rect.x += dx * GRID_SIZE
                    player_rect.y += dy * GRID_SIZE

    # Check if the player has reached the goal
    if player_rect.colliderect(pygame.Rect(goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)):
        print("Congratulations! You solved the maze!")
        running = False

    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
