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
GREEN = (0, 255, 0)

# Maze settings
cols, rows = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Player settings
player_x, player_y = 0, 0
player_rect = pygame.Rect(player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

# Goal settings
goal_x, goal_y = cols - 1, rows - 1

# Movement directions
directions = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Toggle state for solver
show_solver = False
solution_path = []


def create_maze_with_prims():
    """Generate a maze using Prim's algorithm."""
    global maze
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # Start at the player's position
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0  # Mark start as a path

    # List of walls (adjacent cells to paths)
    walls = [(start_x + dx, start_y + dy) for dx, dy in directions.values() if 0 <= start_x + dx < cols and 0 <= start_y + dy < rows]

    while walls:
        # Randomly select a wall
        wx, wy = random.choice(walls)
        walls.remove((wx, wy))

        # Check if this wall can become a passage
        adjacent_paths = 0
        for dx, dy in directions.values():
            nx, ny = wx + dx, wy + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                adjacent_paths += 1

        if adjacent_paths == 1:  # Carve the wall if it connects to only one path
            maze[wy][wx] = 0

            # Add neighboring walls to the list
            for dx, dy in directions.values():
                nx, ny = wx + dx, wy + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1 and (nx, ny) not in walls:
                    walls.append((nx, ny))


def draw_maze():
    """Draw the maze."""
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def is_valid_move(x, y):
    """Check if a move is valid (within bounds and not a wall)."""
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0


def solve_maze(x, y, path):
    """Recursive function to find the path from start to goal."""
    if (x, y) == (goal_x, goal_y):  # Reached the goal
        path.append((x, y))
        return True

    if not is_valid_move(x, y) or (x, y) in path:
        return False

    path.append((x, y))

    for dx, dy in directions.values():
        if solve_maze(x + dx, y + dy, path):
            return True

    path.pop()  # Backtrack
    return False


# Generate the maze with a guaranteed solution using Prim's Algorithm
create_maze_with_prims()

# Solve the maze to find the solution path
solve_maze(0, 0, solution_path)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_maze()

    # Draw the solution path if solver is enabled
    if show_solver:
        for x, y in solution_path:
            pygame.draw.rect(screen, GREEN, (x * GRID_SIZE + 5, y * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))

    # Draw the player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw the goal
    pygame.draw.rect(screen, RED, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle arrow key movement
        elif event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_UP:
                dx, dy = 0, -1
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, 1
            elif event.key == pygame.K_LEFT:
                dx, dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = 1, 0

            new_x = player_rect.x // GRID_SIZE + dx
            new_y = player_rect.y // GRID_SIZE + dy

            if is_valid_move(new_x, new_y):
                player_rect.x += dx * GRID_SIZE
                player_rect.y += dy * GRID_SIZE

            # Handle toggling solver visibility
            if event.key == pygame.K_s:
                show_solver = not show_solver
                print(f"Solver toggled: {'ON' if show_solver else 'OFF'}")

    # Check if the player has reached the goal
    if player_rect.colliderect(pygame.Rect(goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)):
        print("Congratulations! You solved the maze!")
        running = False

    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
