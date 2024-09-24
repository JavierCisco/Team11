import pygame
import sys
import socket

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
    splash_sound = pygame.mixer.Sound("theme.mp3")
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

# UDP Client function
def add_player_transmit(id, codename, equipment_code):
	print(f"Adding player: Id = {id}, Codename = {codename}")
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('localhost', 7500)
	message = f"Equipment code for {codename} is {equipment_code}"
	client_socket.sendto(message, server_address)

	print(f"Transmitted equipment code '{equipment_code}' for player {codename}")
	client_socket.close()
    
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

button_width = 90  # width 
button_height = 50  # height
button_margin = 10  # margin
y_position = SCREEN_HEIGHT - button_height - 20  # Y-position

buttons = [
    Button("F1\nEdit Game", button_margin + 0 * (button_width + button_margin), y_position, button_width, button_height, edit_game),
    Button("F2\nGame Parameters", button_margin + 1 * (button_width + button_margin), y_position, button_width, button_height, game_parameters),
    Button("F3\nStart Game", button_margin + 2 * (button_width + button_margin), y_position, button_width, button_height, start_game),
    Button("F5\nPreEntered Games", button_margin + 3 * (button_width + button_margin), y_position, button_width, button_height, pre_entered_games),
    Button("F7", button_margin + 4 * (button_width + button_margin), y_position, button_width, button_height),
    Button("F8\nView Game", button_margin + 5 * (button_width + button_margin), y_position, button_width, button_height, view_game),
    Button("F10\nFlick Sync", button_margin + 6 * (button_width + button_margin), y_position, button_width, button_height, flick_sync),
    Button("F12\nClear Game", button_margin + 7 * (button_width + button_margin), y_position, button_width, button_height, clear_game),
]

# dictionary to map keys to actions
key_to_action = {
    pygame.K_F1: edit_game,
    pygame.K_F2: game_parameters,
    pygame.K_F3: start_game,
    pygame.K_F5: pre_entered_games,
    pygame.K_F7: lambda: print("F7 clicked!"),  # no action assigned for F7 yet
    pygame.K_F8: view_game,
    pygame.K_F10: flick_sync,
    pygame.K_F12: clear_game
}

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
                
        # check for keypress events
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_action:
                key_to_action[event.key]()
            elif event.key == pygame.K_i:
                id = int(input("Enter player ID: "))
                codename = input("Enter player codename: ").strip()
                equipment_code = input(f"Enter equipment code for {codename: }")
                add_player_transmit(id, codename, equipment_code)


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
