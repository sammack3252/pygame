import os.path
import pygame

scriptDir = os.path.dirname(os.path.abspath(__file__))

class Button: #used for icons
    def __init__(self, x, y, image_name):
        self.x = x
        self.y = y
        self.image = image_name
        self.rect = self.image.get_rect()
        self.image_rect = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width, self.rect.height)

class Game:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.background_color = "white"
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

    def draw_everything(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.buttons_bar_color, pygame.Rect(0, 0, self.width, self.buttons_bar_height))
        self.screen.blit(self.food_button.image, self.food_button.image_rect)
        self.screen.blit(self.cart_button.image, self.cart_button.image_rect)
        self.screen.blit(self.hanger_button.image, self.hanger_button.image_rect)
        self.screen.blit(self.stats_button.image, self.stats_button.image_rect)

        pygame.display.update()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            self.draw_everything()
            self.clock.tick(self.clock_tick)

pygame.init()
game = Game()
game.run()
