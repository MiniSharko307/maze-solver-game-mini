import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 610  # Increased width to fit the border
SCREEN_HEIGHT = 610  # Increased height to fit the border
GRID_SIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BORDER_COLOR = (255, 255, 255)  # Color for the border
FOV_COLOR = (50, 50, 50)  # Color for the Fog of War (non-visible parts)
STATIC_COLOR = (255, 255, 255)  # White static

# Maze settings
cols, rows = (SCREEN_WIDTH - 10) // GRID_SIZE, (SCREEN_HEIGHT - 10) // GRID_SIZE  # Adjust cols/rows to fit inside window
maze = [[1 for _ in range(cols)] for _ in range(rows)]  # Start with all walls

# Player settings
player_x, player_y = 0, 0
player_rect = pygame.Rect(player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

# Goal settings
goal_x, goal_y = cols - 1, rows - 1  # Set the goal near the bottom-right corner

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

# Field of view (AoE) settings
VISION_RADIUS = 3  # Number of cells the player can see in each direction

def create_maze_with_recursive_backtracking():
    """Generate a maze using recursive backtracking."""
    global maze
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # Reset maze to walls

    # Start at the player's position
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0  # Mark start as a path

    # Create a stack for the recursive backtracking
    stack = [(start_x, start_y)]
    
    # Directions for moving (up, down, left, right)
    move_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Randomize the directions to ensure more randomness
    random.shuffle(move_directions)

    while stack:
        x, y = stack[-1]

        # Get all valid neighboring cells (only those that are within bounds and are walls)
        neighbors = []
        for dx, dy in move_directions:
            nx, ny = x + dx * 2, y + dy * 2  # Move in steps of 2 to avoid revisiting immediate neighbors
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            # Choose a random neighbor to visit
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0  # Carve the path
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0  # Carve the wall between the current and next cell
            stack.append((nx, ny))  # Push the neighbor to the stack
        else:
            stack.pop()  # Backtrack if no valid neighbors

    # Ensure the goal is reachable and set the goal position in the bottom-right
    maze[goal_y][goal_x] = 0

    # Carve a path to the goal from the start position
    carve_path_to_goal(start_x, start_y, goal_x, goal_y)

def carve_path_to_goal(start_x, start_y, goal_x, goal_y):
    """Carve a path to the goal to ensure it's reachable."""
    path_x, path_y = start_x, start_y

    # Simple carving to guarantee connection
    while path_x != goal_x or path_y != goal_y:
        if path_x < goal_x:
            path_x += 1
        elif path_x > goal_x:
            path_x -= 1
        if path_y < goal_y:
            path_y += 1
        elif path_y > goal_y:
            path_y -= 1
        maze[path_y][path_x] = 0

def draw_maze():
    """Draw the maze with field of vision (AoE)."""
    # Draw the fog of war (non-visible area)
    for y in range(rows):
        for x in range(cols):
            # Only draw fog outside of the vision range
            if not (player_x - VISION_RADIUS <= x <= player_x + VISION_RADIUS and player_y - VISION_RADIUS <= y <= player_y + VISION_RADIUS):
                pygame.draw.rect(screen, FOV_COLOR, (x * GRID_SIZE + 5, y * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))

    # Draw the visible portion of the maze (within AoE)
    for y in range(max(0, player_y - VISION_RADIUS), min(rows, player_y + VISION_RADIUS + 1)):
        for x in range(max(0, player_x - VISION_RADIUS), min(cols, player_x + VISION_RADIUS + 1)):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE + 5, y * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))  # Adjust position to fit inside

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

def draw_static_effect():
    """Draw random static noise over the screen."""
    for y in range(0, SCREEN_HEIGHT, 10):  # Simplified static for debugging
        for x in range(0, SCREEN_WIDTH, 10):
            if random.random() < 0.05:  # 5% chance to draw static on each cell
                pygame.draw.rect(screen, STATIC_COLOR, (x + random.randint(0, 5), y + random.randint(0, 5), 3, 3))

# Generate the maze with a guaranteed solution using Recursive Backtracking
create_maze_with_recursive_backtracking()

# Solve the maze to find the solution path
solve_maze(0, 0, solution_path)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Draw the border around the game screen
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)  # 5-pixel border

    # Draw the maze with limited field of vision
    draw_maze()

    # Draw the static effect (analog horror effect)
    draw_static_effect()

    # Draw the solution path if solver is enabled
    if show_solver:
        for x, y in solution_path:
            pygame.draw.rect(screen, GREEN, (x * GRID_SIZE + 5, y * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))

    # Draw the player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw the goal
    pygame.draw.rect(screen, RED, (goal_x * GRID_SIZE + 5, goal_y * GRID_SIZE + 5, GRID_SIZE - 10, GRID_SIZE - 10))

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

            new_x, new_y = player_x + dx, player_y + dy
            if is_valid_move(new_x, new_y):
                player_x, player_y = new_x, new_y
                player_rect.x = player_x * GRID_SIZE
                player_rect.y = player_y * GRID_SIZE

            # Toggle solver on/off
            if event.key == pygame.K_s:
                show_solver = not show_solver

    pygame.display.flip()
    clock.tick(30)  # Set the frame rate

pygame.quit()
sys.exit()
