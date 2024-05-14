import pygame
import random
import os.path

scriptDir = os.path.dirname(os.path.abspath(__file__))

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Load snake image
snake_image = pygame.image.load(os.path.join(scriptDir, "graphics", "snakey.png"))
snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))

# Helper functions
def draw_snake(snake):
    for segment in snake:
        screen.blit(snake_image, segment)

def draw_food(food_position):
    pygame.draw.rect(screen, RED, (*food_position, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    if not snake:
        return snake  # If snake is empty, return the unchanged snake

    head = snake[0]
    x, y = head[0], head[1]

    if direction == 'UP':
        y -= CELL_SIZE
    elif direction == 'DOWN':
        y += CELL_SIZE
    elif direction == 'LEFT':
        x -= CELL_SIZE
    elif direction == 'RIGHT':
        x += CELL_SIZE

    new_head = (x, y)
    snake.insert(0, new_head)
    return snake

#spawns a new food
def generate_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return (x, y)

#sees if snake hit a wall
def check_collision(snake):
    head_x, head_y = snake[0]
    # Check if snake hits the screen boundaries
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        return True
    return False

# Game variables
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = 'RIGHT'
food_position = generate_food()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    screen.fill(BLACK)

    # Move snake
    snake = move_snake(snake, direction)

    # Check for collision with food
    if snake[0] == food_position:
        food_position = generate_food()
    else:
        snake.pop()

    # Check for collision with boundaries
    if check_collision(snake):
        running = False  # Game ends if snake hits the screen boundaries

    # Draw snake and food
    draw_snake(snake)
    draw_food(food_position)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
