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
            # elif event.key == pygame.K_i:
            #     id = int(input("Enter player ID: "))
            #     codename = input("Enter player codename: ").strip()
            #     equipment_code = input(f"Enter equipment code for {codename}: ")
            #     add_player_transmit(id, codename, equipment_code)


    if on_splash_screen:
        # display the splash screen with image
        screen.fill((0, 0, 0))
        screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) // 2, 50))
        pygame.display.update()
    else:
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
        for button in buttons:
            button.draw()
        pygame.display.update()

end_game
