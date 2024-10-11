import sys
import pygame
import random
from database import *
from socks import *

# initializing pygame
pygame.init()
pygame.mixer.init()



################################################################################################################################################
# SPLASH SCREEN 
################################################################################################################################################

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Splash Screen")

# load and display the splash image
try:
    splash_sound = pygame.mixer.Sound("theme.mp3")
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (800, 500))
except Exception as error:
    print(f"Error in Splash Screen: {error}")
    pygame.quit()
    sys.exit()
splash_sound.play()
# set a timer to show the main screen after 3 seconds
show_main_screen_event = pygame.USEREVENT + 1
pygame.time.set_timer(show_main_screen_event, 3000)

################################################################################################################################################



################################################################################################################################################
# TABLE + TEXTBOX SET UP
################################################################################################################################################

# TextBox class for table cells
class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('black')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.font = pygame.font.Font(None, 20)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(100, text_surface.get_width() + 10)

# Create two tables of text boxes (2 columns x 10 rows each)
table1 = []
table2 = []
cell_width = 100
cell_height = 40

# Table 1 (left side - columns 1 and 2)
for row in range(10):
    table_row = []
    for col in range(2):
        x = 100 + col * cell_width
        y = 50 + row * cell_height
        table_row.append(TextBox(x, y, cell_width, cell_height))
    table1.append(table_row)

# Table 2 (right side - columns 3 and 4)
for row in range(10):
    table_row = []
    for col in range(2):
        x = 450 + col * cell_width
        y = 50 + row * cell_height
        table_row.append(TextBox(x, y, cell_width, cell_height))
    table2.append(table_row)

# Combine both tables
tables = [table1, table2]

################################################################################################################################################



################################################################################################################################################
# BUTTON CLASS
################################################################################################################################################

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text_lines = text.split('\n')
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 20)

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

################################################################################################################################################



################################################################################################################################################
# FUNCTIONS CALLED IN MAIN.PY
################################################################################################################################################

# BUTTONS INGAME
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

# INTERACT WITH DATABASE.PY 
def add_player():
    player_id = random.randint(1000, 9999)  # This would be dynamically generated or provided
    send_equipment_code(player_id)
    name = input('Name of player?:')
    insert_player(player_id, name)
    print(f"Added:\nName: {name}\nID: {player_id}")

def delete_player():
    playID = input('ID of player to remove?:')
    remove_player(playID)
    print(f'Player {playID} removed!')

# TERMINATE GAME - CALLED IN MAIN.PY
def end_game():
    bye_data()
    pygame.quit()
    bye_socks()
    sys.exit()

# simply used to test things we are trying to make work ULtra secret
def test_func():
# usable with 'v' for now just used to view table players
    view_database()

################################################################################################################################################



################################################################################################################################################
# BUTTONS AND THEIR ACTIONS
################################################################################################################################################

#Button dimensions
button_width = 100   
button_height = 60
button_margin = 10
y_position = SCREEN_HEIGHT - button_height - 80

buttons = [
    Button("F1\nEdit Game", button_margin + 0 * (button_width + button_margin), y_position, button_width, button_height, edit_game),
    Button("F2\nGame\nParameters", button_margin + 1 * (button_width + button_margin), y_position, button_width, button_height, game_parameters),
    Button("F3\nStart Game", button_margin + 2 * (button_width + button_margin), y_position, button_width, button_height, start_game),
    Button("F5\nPreEntered Games", button_margin + 3 * (button_width + button_margin), y_position, button_width, button_height, pre_entered_games),
    Button("F7\nTBD", button_margin + 4 * (button_width + button_margin), y_position, button_width, button_height),
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
    pygame.K_F12: clear_game,
    pygame.K_i: add_player,
    pygame.K_BACKSPACE: delete_player,
    pygame.K_ESCAPE: end_game,
    pygame.K_t: test_func
}

################################################################################################################################################
