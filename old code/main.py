import os.path
import pygame
import pygame.freetype
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

class Game:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.background_color = "PINK"
        self.buttons_bar_height = 100
        self.buttons_bar_color = "orange"

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Pal")

        self.clock_tick = 60
        self.clock = pygame.time.Clock()

        #icons
        foodIcon = pygame.image.load(os.path.join(scriptDir, "graphics", "Icon_Food.png"))
        foodIcon = pygame.transform.scale(foodIcon, (75, 75))
        self.food_button = Button(self.width/8, self.buttons_bar_height/2, foodIcon)

        cartIcon = pygame.image.load(os.path.join(scriptDir, "graphics", "Icon_Cart.png"))
        cartIcon = pygame.transform.scale(cartIcon, (75, 75))
        self.cart_button = Button((self.width/8 * 3), self.buttons_bar_height/2, cartIcon)

        hangerIcon = pygame.image.load(os.path.join(scriptDir, "graphics", "Icon_Hanger.png"))
        hangerIcon = pygame.transform.scale(hangerIcon, (75, 75))
        self.hanger_button = Button((self.width/8 * 5), self.buttons_bar_height/2, hangerIcon)

        statsIcon = pygame.image.load(os.path.join(scriptDir, "graphics", "Icon_Stats.png"))
        statsIcon = pygame.transform.scale(statsIcon, (75, 75))
        self.stats_button = Button((self.width/8 * 7), self.buttons_bar_height/2, statsIcon)


        #snakey
        snakeIcon = pygame.image.load(os.path.join(scriptDir, "graphics", "snakey.png"))
        snakeIcon = pygame.transform.scale(snakeIcon, (400, 400))
        self.snake_button = Button((250), 300, snakeIcon)

    def draw_everything(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.buttons_bar_color, pygame.Rect(0, 0, self.width, self.buttons_bar_height))
        self.screen.blit(self.food_button.image, self.food_button.image_rect)
        self.screen.blit(self.cart_button.image, self.cart_button.image_rect)
        self.screen.blit(self.hanger_button.image, self.hanger_button.image_rect)
        self.screen.blit(self.stats_button.image, self.stats_button.image_rect)
        self.screen.blit(self.snake_button.image, self.snake_button.image_rect)

        pygame.display.update()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            self.draw_everything()
            self.clock.tick(self.clock_tick)

def play(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=PINK,
        text_rgb=BROWN,
        text="Return to main menu",
        action=GameState.TITLE,
    )
    game = Game()
    game.run()

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(PINK)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action

        pygame.display.flip()

#end massive game chunk ^^


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    CREDITS = 2

#call main when the script is run
if __name__ == "__main__":
    main()
