import pygame
import sys
import socket
import random
import subprocess
from database import *

# initializing pygame
pygame.init()
pygame.mixer.init()

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
    print("Error in Splash Screen: {error}")
    pygame.quit()
    sys.exit()
splash_sound.play()
# set a timer to show the main screen after 3 seconds
show_main_screen_event = pygame.USEREVENT + 1
pygame.time.set_timer(show_main_screen_event, 3000)

# Functions to start the server and client
def start_server():
    subprocess.Popen(['python3', 'server.py'])  # Start the UDP server

def start_client():
    subprocess.Popen(['python3', 'client.py'])  # Start the UDP client

# Call these functions to start the server and client
start_server()
start_client()

# UDP setup
UDP_IP = "127.0.0.1"  # replace with your target IP
UDP_PORT = 7500       # the port to broadcast equipment codes
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_equipment_code(code):
    message = str(code).encode('utf-8')
    udp_socket.sendto(message, (UDP_IP, UDP_PORT))
    print(f"Sent equipment code: {code}")

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

# button class
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
    

# button action functions
def edit_game():
    print("Edit Game clicked!")

def game_parameters():
    print("Game Parameters clicked!")

# Countdown variables
countdown_active = False
countdown_time = 30  # 30 seconds countdown
start_ticks = 0  # tracks when countdown started

def start_game():
    print("Start Game clicked!")
    global countdown_active, start_ticks
    countdown_active = True  # Start the countdown
    start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
    print("Countdown started!")

def pre_entered_games():
    print("PreEntered Games clicked!")

def view_game():
    print("View Game clicked!")

def flick_sync():
    print("Flick Sync clicked!")

def clear_game():
    print("Clear Game clicked!")

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

def end_game():
    bye_data()	
    pygame.quit()
    udp_socket.close()
    sys.exit()

def test_func():
# usable with 't' for now just used to view table players
    view_database()

button_width = 100  # width 
button_height = 60  # height
button_margin = 10  # margin
y_position = SCREEN_HEIGHT - button_height - 80  # Y-position

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

# main loop
running = True
on_splash_screen = True
entry_screen_active = True
play_action = True

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
        
        # Handle events for text boxes in the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.handle_event(event)

    #splash screen
    if on_splash_screen:
        # display the splash screen with image
        screen.fill((0, 0, 0))
        screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) // 2, 50))
        pygame.display.update()
    
    #countdown screen
    elif countdown_active:
        # Handle the countdown
        entry_screen_active = False
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        countdown_left = max(countdown_time - seconds_passed, 0)

        # Display countdown
        screen.fill((255, 255, 255))  # White background
        font = pygame.font.Font(None, 100)
        countdown_text = font.render(str(countdown_left), True, (0, 0, 0))  # Black countdown
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()

        # check if countdown is finished
        if countdown_left <= 0:
            print("Countdown ended")
            countdown_active = False
            play_action = True
        
    #entry screen
    elif entry_screen_active:
        # draw buttons screen
        screen.fill((255, 255, 255))
        ###################################################
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        pygame.display.set_caption("Entry Terminal")
        font = pygame.font.Font(None, 36)
        text = font.render("Edit Current Game",True, BLACK)
        screen.blit(text, (280, 0))
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 550, 800, 40))
        text = font.render("<Del> to Delete Player, <i> to Insert Player or Edit Codename", True, WHITE)
        screen.blit(text, (50,560))
        ###################################################

        # draw column labels (left)
        label_font = pygame.font.Font(None, 24)
        name_label_left = label_font.render("Name", True, BLACK)
        id_label_left = label_font.render("ID", True, BLACK)
        screen.blit(name_label_left, (100, 30))
        screen.blit(id_label_left, (200, 30)) 
        # draw column labels (right)
        name_label_right = label_font.render("Name", True, BLACK)
        id_label_right = label_font.render("ID", True, BLACK)
        screen.blit(name_label_right, (450, 30)) 
        screen.blit(id_label_right, (550, 30)) 
  
        # draw the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.draw(screen)
                    
        for button in buttons:
            button.draw()
        pygame.display.update()

    # game action screen
    elif play_action:
            # Display a screen with half green and half red
            screen.fill((0, 255, 0), pygame.Rect(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))  # Green left half
            screen.fill((255, 0, 0), pygame.Rect(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))  # Red right half
            pygame.display.update()
        
end_game
