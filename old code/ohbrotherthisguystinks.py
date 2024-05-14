import os.path
import pygame
import pygame.freetype
import random
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

scriptDir = os.path.dirname(os.path.abspath(__file__))

PINK = (227, 193, 232)
BROWN = (125, 110, 79)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    #returns surface with text written on
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    #a user interface element that can be added to a surface
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False #indicates if the mouse is over the element

        #create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        #create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        #add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        #assign button action
        self.action = action

        #calls the init method of the parent sprite class
        super().__init__()

#properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        #updates the elemtn's appearance depending on the mouse position and returns the button's action if clicked
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        #draws element onto a surface
        surface.blit(self.image, self.rect)

class Button:
    def __init__(self, x, y, image_name):
        self.x = x
        self.y = y
        self.image = image_name
        self.rect = self.image.get_rect()
        self.image_rect = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width, self.rect.height)

def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Python Pal")
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play(screen)
        
        if game_state == GameState.CREDITS:
            game_state = credits(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    start_btn = UIElement(
        center_position=(250, 300),
        font_size=30,
        bg_rgb=PINK,
        text_rgb=BROWN,
        text="Start",
        action=GameState.NEWGAME,
    )

    quit_btn = UIElement(
        center_position=(250, 400),
        font_size=30,
        bg_rgb=PINK,
        text_rgb=BROWN,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]
    #snakey

    #main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(PINK)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


#everything to do w the actual game vv
class Game():
    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 20
    FPS = 10

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    # Load snake image
    snake_image = pygame.image.load(os.path.join(scriptDir, "graphics", "snakey.png"))
    snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))

    # Helper functions
    def draw_snake(snake, self):
        for segment in snake:
            self.screen.blit(self.snake_image, segment)

    def draw_food(food_position, self):
        pygame.draw.rect(self.screen, self.RED, (*food_position, self.CELL_SIZE, self.CELL_SIZE))

    def move_snake(snake, direction, self):
        if not snake:
            return snake  # If snake is empty, return the unchanged snake

        head = snake[0]
        x, y = head[0], head[1]

        if direction == 'UP':
            y -= self.CELL_SIZE
        elif direction == 'DOWN':
            y += self.CELL_SIZE
        elif direction == 'LEFT':
            x -= self.CELL_SIZE
        elif direction == 'RIGHT':
            x += self.CELL_SIZE

        new_head = (x, y)
        snake.insert(0, new_head)
        return snake

    def generate_food(self):
        x = random.randint(0, (self.WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
        y = random.randint(0, (self.HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
        return (x, y)

    def check_collision(snake, self):
        head_x, head_y = snake[0]
        # Check if snake hits the screen boundaries
        if head_x < 0 or head_x >= self.WIDTH or head_y < 0 or head_y >= self.HEIGHT:
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


#end massive game chunk ^^


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    CREDITS = 2

#call main when the script is run
if __name__ == "__main__":
    main()
