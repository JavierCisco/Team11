import pygame
import sys

pygame.init()
pygame.mixer.init()
# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Splash Screen")

# load and display the splash image
try:
    splash_sound = pygame.mixer.Sound("theme.wav")
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (800, 500))
except pygame.error:
    print("Error: logo.png not found.")
    pygame.quit()
    sys.exit()
splash_sound.play()
# set a timer to show the main screen after 3 seconds
show_main_screen_event = pygame.USEREVENT + 1
pygame.time.set_timer(show_main_screen_event, 3000)

# button class
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text_lines = text.split('\n')
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 26)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  #draw buttons rectangle
        for i, line in enumerate(self.text_lines):
            button_text = self.font.render(line, True, (255, 255, 255))
            text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
            text_y = self.rect.y + (self.rect.height - (len(self.text_lines) * self.font.get_height())) // 2 + i * self.font.get_height()
            screen.blit(button_text, (text_x, text_y))

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()  # call action if button is clicked (fix so it's connected to keyboard)

# button action functions
def edit_game():
    print("Edit Game clicked!")

def game_parameters():
    print("Game Parameters clicked!")

def start_game():
    print("Start Game clicked!")

def pre_entered_games():
    print("PreEntered Games clicked!")

def view_game():
    print("View Game clicked!")

def flick_sync():
    print("Flick Sync clicked!")

def clear_game():
    print("Clear Game clicked!")

# create buttons
buttons = [
    Button("F1\nEdit Game", (SCREEN_WIDTH - 200) // 2, 100, 200, 50, edit_game),
    Button("F2\nGame Parameters", (SCREEN_WIDTH - 200) // 2, 170, 200, 50, game_parameters),
    Button("F3\nStart Game", (SCREEN_WIDTH - 200) // 2, 240, 200, 50, start_game),
    Button("F5\nPreEntered Games", (SCREEN_WIDTH - 200) // 2, 310, 200, 50, pre_entered_games),
    Button("F7", (SCREEN_WIDTH - 200) // 2, 380, 200, 50),
    Button("F8\nView Game", (SCREEN_WIDTH - 200) // 2, 450, 200, 50, view_game),
    Button("F10\nFlick Sync", (SCREEN_WIDTH - 200) // 2, 520, 200, 50, flick_sync),
    Button("F12\nClear Game", (SCREEN_WIDTH - 200) // 2, 590, 200, 50, clear_game),
]

# main loop
running = True
on_splash_screen = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == show_main_screen_event and on_splash_screen:
            on_splash_screen = False
            
        # check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for button in buttons:
                button.is_clicked(mouse_pos)

    if on_splash_screen:
        # display the splash screen with image
        screen.fill((0, 0, 0))
        screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) // 2, 50))
        pygame.display.update()
    else:
        # draw buttons screen
        screen.fill((255, 255, 255))
        for button in buttons:
            button.draw()
        pygame.display.update()

pygame.quit()
sys.exit()
